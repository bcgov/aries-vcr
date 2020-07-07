
import requests

from django.conf import settings
from django.core.management.base import BaseCommand

from api_v2.models.Topic import Topic

from asgiref.sync import async_to_sync


class Command(BaseCommand):
    help = "Delete data for a single Topic."

    def add_arguments(self, parser):
        parser.add_argument('topic_id', type=str)

    def handle(self, *args, **options):
        self.delete_topic(*args, **options)

    @async_to_sync
    async def delete_topic(self, *args, **options):
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
                        self.stdout.write(" ... " + credential.wallet_id + " ...")
                        self.stdout.write(" ... TODO in aries-vcr ...")
                        # try:
                        #     response = requests.get(
                        #         f"{settings.AGENT_ADMIN_URL}/credential/{credential.wallet_id}",
                        #         headers=settings.ADMIN_REQUEST_HEADERS,
                        #     )
                        #     response.raise_for_status()
                        #     credential = response.json()
                        # except Exception as e:
                        #     pass

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
            self.stdout.write("Done.")


