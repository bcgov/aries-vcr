from django.core.management.base import BaseCommand, CommandError
from django.db import transaction, DEFAULT_DB_ALIAS
from django.db.models import signals

from api_v2.indy.credential import CredentialManager

from api_v2.models.Address import Address
from api_v2.models.Attribute import Attribute
from api_v2.models.Credential import Credential
from api_v2.models.Name import Name

from tob_anchor.solrqueue import SolrQueue

MODEL_TYPE_MAP = {
    "address": Address,
    "attribute": Attribute,
    "category": Attribute,
    "name": Name,
}


class Command(BaseCommand):
    help = "Reprocesses all credentials to populate search database"

    def handle(self, *args, **options):
        queue = SolrQueue()
        with queue:
            self.reprocess(queue, *args, **options)

    def reprocess(self, queue, *args, **options):
        self.stdout.write("Starting...")

        cred_count = Credential.objects.count()
        self.stdout.write("Reprocessing {} credentials".format(cred_count))

        current_cred = 0
        for credential in Credential.objects.all().iterator():
            with transaction.atomic():
                current_cred += 1
                self.stdout.write(
                    "Processing credential id: {} ({} of {})".format(
                        credential.id, current_cred, cred_count
                    )
                )

                credential_type = credential.credential_type
                processor_config = credential_type.processor_config
                mapping = processor_config.get("mapping") or []

                # Delete existing search models
                for model_key, model_cls in MODEL_TYPE_MAP.items():
                    if model_key == "category":
                        continue
                    # Don't trigger search reindex (yet)
                    model_cls.objects.filter(credential=credential)._raw_delete(using=DEFAULT_DB_ALIAS)

                # Create search models using mapping from issuer config
                for model_mapper in mapping:
                    model_name = model_mapper["model"]

                    model_cls = MODEL_TYPE_MAP[model_name]
                    model = model_cls()
                    for field, field_mapper in model_mapper["fields"].items():
                        setattr(
                            model,
                            field,
                            CredentialManager.process_mapping(field_mapper, credential),
                        )
                    if model_name == "category":
                        model.format = "category"

                    # skip blank values
                    if model_name == "name" and (model.text is None or model.text is ""):
                        continue
                    if (model_name == "category" or model_name == "attribute") and \
                            (not model.type or model.value is None or model.value is ""):
                        continue

                    model.credential = credential
                    model.save()

                # Now reindex
                signals.post_save.send(sender=Credential, instance=credential, using=DEFAULT_DB_ALIAS)
