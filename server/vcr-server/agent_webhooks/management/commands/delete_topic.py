
import time

import requests
from api.v2.models.Topic import Topic
from asgiref.sync import async_to_sync
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Delete data for a single Topic."

    def add_arguments(self, parser):
        parser.add_argument('topic_id', type=str)

    def handle(self, *args, **options):
        self.delete_topic(*args, **options)

    @async_to_sync
    async def delete_topic(self, *args, **options):
        start_time = time.perf_counter()

        # get Topic ID from input parameters
        topic_id = options['topic_id']
        self.stdout.write("Deleting topic_id: " + topic_id)

        # delete credentials for Topic from wallet (we need to do this first)
        selected_topics = Topic.objects.filter(source_id=topic_id).all()
        if 0 < len(selected_topics):
            for topic in selected_topics:
                if 0 < len(topic.credentials.all()):
                    self.stdout.write("Deleting wallet credentials ...")
                    for credential in topic.credentials.all():
                        self.stdout.write(" ... " + credential.credential_id + " ...")
                        try:
                            response = requests.delete(
                                f"{settings.AGENT_ADMIN_URL}/credential/{credential.credential_id}",
                                headers=settings.ADMIN_REQUEST_HEADERS,
                            )
                            response.raise_for_status()
                        except Exception as e:
                            self.stdout.write("Error removing wallet credential " + credential.credential_id)
                            pass

        # delete Topic from OrgBook database (also clears out Solr indexes)
        self.stdout.write("Deleting topic from OrgBook search database ...")
        selected_topics = Topic.objects.filter(source_id=topic_id).all()
        if 0 == len(selected_topics):
            self.stdout.write(" ... topic_id not found in OrgBook.")
        else:
            for topic in selected_topics:
                if 0 < len(topic.related_to.all()):
                    self.stdout.write(" ... deleting related ...")
                    for related in topic.related_to.all():
                        related.delete()
                self.stdout.write(" ... deleting topic ...")
                topic.delete()
            
            # Update search indexes to refresh facets
            self.stdout.write("Updating search indexes to refresh facets ...")
            try:
                # Call the update_index management command to refresh facets
                # This ensures facets no longer reference the deleted topic
                call_command(
                    'update_index',
                    age=1,  # Update recent changes to catch references
                    verbosity=0  # Reduce verbosity to avoid excessive output
                )
                self.stdout.write(" ... search index update completed.")
            except Exception as e:
                self.stdout.write(
                    f"Warning: Search index update failed: {str(e)}. "
                    "You may need to manually run 'update_index' to refresh "
                    "facets."
                )
            
            self.stdout.write("Done.")

        processing_time = time.perf_counter() - start_time
        self.stdout.write(f"Processing time: {processing_time} sec")
