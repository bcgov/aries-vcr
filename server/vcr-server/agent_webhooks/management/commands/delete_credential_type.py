import time

import requests
from api.v2.models.Credential import Credential
from api.v2.models.CredentialSet import CredentialSet
from api.v2.models.CredentialType import CredentialType
from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete data for a single Credential Type."

    def add_arguments(self, parser):
        parser.add_argument('credential_type_id', type=str)

    def handle(self, *args, **options):
        self.delete_credential_type(*args, **options)

    def delete_credential_type(self, *args, **options):
        start_time = time.perf_counter()

        # get Credential Type ID from input parameters
        credential_type_id = options['credential_type_id']
        self.stdout.write("Deleting credential_type_id: " + credential_type_id)

        # Find the credential type
        try:
            credential_type = CredentialType.objects.get(id=credential_type_id)
        except CredentialType.DoesNotExist:
            self.stdout.write(" ... credential_type_id not found in OrgBook.")
            return

        # Find all credentials for this credential type
        credentials = Credential.objects.filter(
            credential_type=credential_type
        )

        # delete credentials from wallet first
        if credentials.exists():
            self.stdout.write("Deleting wallet credentials ...")
            for credential in credentials:
                self.stdout.write(
                    " ... " + credential.credential_id + " ..."
                )
                try:
                    response = requests.delete(
                        f"{settings.AGENT_ADMIN_URL}/credential/"
                        f"{credential.credential_id}",
                        headers=settings.ADMIN_REQUEST_HEADERS,
                    )
                    response.raise_for_status()
                except Exception:
                    self.stdout.write(
                        "Error removing wallet credential "
                        + credential.credential_id
                    )
                    pass

        # delete Credential Type from OrgBook database (clears Solr indexes)
        self.stdout.write(
            "Deleting credential type from OrgBook search database ..."
        )

        # Delete all credentials associated with this credential type
        if credentials.exists():
            self.stdout.write(" ... deleting credentials ...")
            # Django CASCADE will handle deleting related objects:
            # - topic_rels (TopicRelationship)
            # - attributes (Attribute)
            # - names (Name)
            # - claims (Claim)
            # - addresses (Address)
            credentials.delete()
        
        # Delete credential sets associated with this credential type
        credential_sets = CredentialSet.objects.filter(
            credential_type=credential_type
        )
        if credential_sets.exists():
            self.stdout.write(" ... deleting credential sets ...")
            credential_sets.delete()
        
        # Finally, delete the credential type itself
        self.stdout.write(" ... deleting credential type ...")
        credential_type.delete()
        self.stdout.write("Done.")

        processing_time = time.perf_counter() - start_time
        self.stdout.write(f"Processing time: {processing_time} sec")
