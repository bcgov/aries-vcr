from django.core.management.base import BaseCommand, CommandError
from django.db import transaction

from api_v2.models.Address import Address
from api_v2.models.Attribute import Attribute
from api_v2.models.Category import Category
from api_v2.models.Credential import Credential
from api_v2.models.Name import Name

from api_v2.indy.credential import CredentialManager


MODEL_TYPE_MAP = {
    "address": Address,
    "attribute": Attribute,
    "category": Category,
    "name": Name,
}


class Command(BaseCommand):
    help = "Reprocesses all credentials to populate search database"

    def handle(self, *args, **options):
        self.stdout.write("Starting...")
        cred_count = Credential.objects.count()
        self.stdout.write("Reprocessing {} credentials".format(cred_count))

        current_cred = 0
        for credential in Credential.objects.all():
            with transaction.atomic():
                current_cred += 1
                self.stdout.write(
                    "Processing credential id:{} ({} of {})".format(
                        credential.id, current_cred, cred_count
                    )
                )

                credential_type = credential.credential_type
                processor_config = credential_type.processor_config
                mapping = processor_config.get("mapping") or []

                # Delete existing search models
                for Model in MODEL_TYPE_MAP.values():
                    Model.objects.filter(credential=credential).delete()

                # Create search models using mapping from issuer config
                for model_mapper in mapping:
                    model_name = model_mapper["model"]

                    Model = MODEL_TYPE_MAP[model_name]
                    model = Model()
                    for field, field_mapper in model_mapper["fields"].items():
                        setattr(
                            model,
                            field,
                            CredentialManager.process_mapping(field_mapper, credential),
                        )

                    model.credential = credential
                    model.save()
