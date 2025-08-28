import time
from datetime import timedelta

import requests
from api.v2.models.Credential import Credential
from api.v2.models.CredentialSet import CredentialSet
from api.v2.models.CredentialType import CredentialType
from django.conf import settings
from django.core.management.base import BaseCommand
from django.utils import timezone
from vcr_server.utils.solrqueue import SolrQueue


class Command(BaseCommand):
    help = "Delete data for a single Credential Type."

    def add_arguments(self, parser):
        parser.add_argument('credential_type_id', type=str)

    def handle(self, *args, **options):
        queue = SolrQueue()
        with queue:
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

        # CRITICAL: Clear Topic caches BEFORE deletion to prevent stale
        # search indexing during signal processing
        self.stdout.write("Clearing topic caches ...")
        self._clear_topic_caches(credential_type_id)

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
        
        # Clean up search index to remove stale references
        self.stdout.write("Cleaning up search index ...")
        self._cleanup_search_index(credential_type_id)
        
        self.stdout.write("Done.")

        processing_time = time.perf_counter() - start_time
        self.stdout.write(f"Processing time: {processing_time} sec")

    def _clear_topic_caches(self, credential_type_id):
        """Clear Topic caches before deletion to prevent stale indexing"""
        try:
            from api.v2.models.Credential import Credential
            from api.v2.models.Topic import Topic

            # Find all topics that have credentials of this type
            topic_ids = set(Credential.objects.filter(
                credential_type_id=credential_type_id
            ).values_list('topic_id', flat=True))
            
            # Also clear caches for ALL topics that might have cached this
            # credential type (even if no active credentials exist)
            # This handles edge cases where credential types with no
            # credentials still appear in facets due to cached data
            all_topics = Topic.objects.all()
            
            self.stdout.write(
                f" ... clearing caches for {len(topic_ids)} affected topics"
            )
            self.stdout.write(
                " ... clearing all topic caches as safety measure"
            )
            
            for topic in all_topics:
                # Clear the cached values for ALL topics to ensure no
                # stale credential_type_id references remain anywhere
                topic._active_cred_ids = None
                topic._active_cred_type_ids = None
                    
            self.stdout.write(" ... topic caches cleared")
            
        except Exception as e:
            self.stdout.write(f" ... warning: cache clearing failed: {str(e)}")

    def _cleanup_search_index(self, credential_type_id):
        """Remove stale Solr documents referencing deleted credential type"""
        try:
            from haystack import connections
            from haystack.backends.solr_backend import SolrSearchBackend

            backend = connections['default'].get_backend()
            if isinstance(backend, SolrSearchBackend):
                # Remove documents referencing the deleted credential_type_id
                queries_to_clean = [
                    f'credential_type_id:{credential_type_id}',
                    f'topic_credential_type_id:{credential_type_id}',
                ]
                
                for query in queries_to_clean:
                    backend.conn.delete(q=query)
                    self.stdout.write(f" ... removed Solr docs: {query}")
                
                # Also need to update Topic index for affected topics
                # that might still have stale credential_type_id references
                self._update_affected_topics(backend, credential_type_id)
                
                # Commit changes and optimize to refresh facet caches
                backend.conn.commit()
                backend.conn.optimize()
                
                self.stdout.write(" ... search index cleanup completed")
            else:
                self.stdout.write(" ... non-Solr backend, skipping cleanup")
                
        except Exception as e:
            self.stdout.write(f" ... warning: search cleanup failed: {str(e)}")

    def _update_affected_topics(self, backend, credential_type_id):
        """Update topic indexes that might still reference deleted cred type"""
        try:
            from api.v2.models.Topic import Topic
            from django.db import DEFAULT_DB_ALIAS
            from django.db.models import signals

            self.stdout.write(
                " ... triggering targeted topic reindexing via signals"
            )
            
            # Strategy 1: Find topics that were actually affected by this
            # credential type by finding topics that had credentials of this
            # type before deletion
            affected_topic_ids = set()
            
            # Since credentials are already deleted, we need to find topics
            # that might still have stale cached references or need refreshed
            # indexes. Look for topics that had recent activity or might be
            # affected
            recent_topics = Topic.objects.filter(
                update_timestamp__gte=timezone.now() - timedelta(hours=24)
            ).values_list('id', flat=True)
            
            affected_topic_ids.update(recent_topics)
            
            # Strategy 2: Also target topics that might have the deleted
            # credential_type_id in their cached data - this is a broader
            # safety net
            all_active_topics = Topic.objects.filter(
                credentials__latest=True,
                credentials__revoked=False
            ).distinct().values_list('id', flat=True)[:500]  # Limit size
            
            affected_topic_ids.update(all_active_topics)
            
            # Retrieve and update affected topics
            topics_to_update = Topic.objects.filter(
                id__in=affected_topic_ids
            ).select_related('foundational_credential')
            
            updated_count = 0
            
            for topic in topics_to_update:
                try:
                    # Clear cached values to force fresh computation
                    topic._active_cred_ids = None
                    topic._active_cred_type_ids = None
                    
                    # Touch the topic to update its timestamp
                    topic.save(update_fields=['update_timestamp'])
                    
                    # Trigger explicit reindexing via signal
                    signals.post_save.send(
                        sender=Topic,
                        instance=topic,
                        using=DEFAULT_DB_ALIAS,
                        created=False
                    )
                    
                    updated_count += 1
                    
                except Exception as e:
                    self.stdout.write(
                        f" ... warning: failed to update topic {topic.pk}: {e}"
                    )
            
            if updated_count > 0:
                self.stdout.write(
                    f" ... triggered reindexing for {updated_count} topics"
                )
            
        except Exception as e:
            self.stdout.write(f" ... warning: topic update failed: {str(e)}")
