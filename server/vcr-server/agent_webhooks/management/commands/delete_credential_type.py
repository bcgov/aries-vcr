import time

import requests
from api.v2.models.Credential import Credential
from api.v2.models.CredentialSet import CredentialSet
from api.v2.models.CredentialType import CredentialType
from django.conf import settings
from django.core.management.base import BaseCommand
from vcr_server.utils.solrqueue import SolrQueue


class Command(BaseCommand):
    help = "Delete data for a single Credential Type."

    def add_arguments(self, parser):
        parser.add_argument('credential_type_id', type=str)

    def handle(self, *args, **options):
        credential_type_id = options['credential_type_id']
        
        # Track affected topics for targeted reindexing
        affected_topics = []
        
        queue = SolrQueue()
        with queue:
            affected_topics = self.delete_credential_type(*args, **options)
            
            # Wait for queue to drain while still in context
            eject = 20
            while queue.qsize() > 0 and eject > 0:
                self.stdout.write(
                    f" ... waiting for Solr queue to drain "
                    f"({queue.qsize()} items left) ..."
                )
                time.sleep(1)
                eject -= 1
            
            if eject == 0:
                self.stdout.write(
                    " ... warning: Solr queue did not drain in time, "
                    "proceeding anyway ..."
                )
        
        # Perform targeted search index refresh
        self.stdout.write("Performing targeted search index refresh ...")
        self._refresh_affected_indexes(credential_type_id, affected_topics)

    def delete_credential_type(self, *args, **options):
        start_time = time.perf_counter()

        # get Credential Type ID from input parameters
        credential_type_id = options['credential_type_id']
        self.stdout.write("Deleting credential_type_id: " + credential_type_id)

        # Track topics affected by this deletion for targeted reindexing
        affected_topics = set()

        # Find the credential type
        try:
            credential_type = CredentialType.objects.get(id=credential_type_id)
        except CredentialType.DoesNotExist:
            self.stdout.write(" ... credential_type_id not found in OrgBook.")
            return list(affected_topics)

        # Find all credentials for this credential type
        credentials = Credential.objects.filter(
            credential_type=credential_type
        )

        # Track topics affected by credential deletion
        if credentials.exists():
            topic_ids = set(credentials.values_list('topic_id', flat=True))
            affected_topics.update(topic_ids)
            self.stdout.write(
                f" ... found {len(topic_ids)} topics affected by "
                f"credential deletion"
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

        # Clear Topic caches BEFORE deletion to prevent stale search indexing
        self.stdout.write("Clearing topic caches ...")
        self._clear_topic_caches(credential_type_id, affected_topics)

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
            # Track additional topics affected by credential set deletion
            cs_topic_ids = set(
                credential_sets.values_list('topic_id', flat=True)
            )
            affected_topics.update(cs_topic_ids)
            self.stdout.write(
                f" ... found {len(cs_topic_ids)} additional topics affected "
                f"by credential set deletion"
            )
            credential_sets.delete()
        
        # Finally, delete the credential type itself
        self.stdout.write(" ... deleting credential type ...")
        credential_type.delete()
        
        self.stdout.write("Done.")

        processing_time = time.perf_counter() - start_time
        self.stdout.write(f"Processing time: {processing_time} sec")
        
        return list(affected_topics)

    def _clear_topic_caches(self, credential_type_id, affected_topics):
        """Clear Topic caches for affected topics to prevent stale indexing"""
        try:
            from api.v2.models.Topic import Topic

            self.stdout.write(
                f" ... clearing caches for {len(affected_topics)} "
                f"affected topics"
            )
            
            # Clear caches for affected topics
            for topic_id in affected_topics:
                try:
                    topic = Topic.objects.get(id=topic_id)
                    topic._active_cred_ids = None
                    topic._active_cred_type_ids = None
                except Topic.DoesNotExist:
                    continue
                    
            self.stdout.write(" ... topic caches cleared")
            
        except Exception as e:
            self.stdout.write(
                f" ... warning: cache clearing failed: {str(e)}"
            )

    def _refresh_affected_indexes(self, credential_type_id, affected_topics):
        """Perform targeted search index refresh for affected topics"""
        try:
            from api.v2.models.Topic import Topic
            from api.v2.search_indexes import CredentialIndex
            from api.v3.indexes.Topic import TopicIndex
            from haystack import connections
            from haystack.backends.solr_backend import SolrSearchBackend

            backend = connections['default'].get_backend()
            if not isinstance(backend, SolrSearchBackend):
                self.stdout.write(" ... non-Solr backend, skipping refresh")
                return

            # 1. Remove stale documents referencing the deleted credential type
            self._cleanup_search_index(credential_type_id)

            # 2. Refresh affected topics in search indexes
            if affected_topics:
                self.stdout.write(
                    f" ... refreshing {len(affected_topics)} affected topics"
                )
                
                # Update TopicIndex for affected topics
                topic_index = TopicIndex()
                topics_to_update = Topic.objects.filter(id__in=affected_topics)
                
                if topics_to_update.exists():
                    self.stdout.write(
                        f" ... updating {len(topics_to_update)} topics "
                        f"in v3 index"
                    )
                    backend.update(topic_index, topics_to_update)

                # Update CredentialIndex for credentials in affected topics
                # This ensures topic_credential_type_id fields are refreshed
                from api.v2.models.Credential import Credential
                credential_index = CredentialIndex()
                affected_credentials = Credential.objects.filter(
                    topic_id__in=affected_topics
                ).select_related('credential_type', 'topic')
                
                if affected_credentials.exists():
                    self.stdout.write(
                        f" ... updating {len(affected_credentials)} "
                        f"credentials in v2 index"
                    )
                    backend.update(credential_index, affected_credentials)

            # 3. Commit and optimize to ensure changes are visible
            backend.conn.commit()
            self.stdout.write(" ... committed search index changes")
            
            backend.conn.optimize()
            self.stdout.write(" ... optimized search index")
            
            self.stdout.write(" ... targeted search index refresh completed")

        except Exception as e:
            self.stdout.write(
                f" ... warning: targeted refresh failed: {str(e)}"
            )
            self.stdout.write(" ... falling back to query-based cleanup")
            self._cleanup_search_index(credential_type_id)

    def _cleanup_search_index(self, credential_type_id):
        """Remove stale Solr documents referencing deleted credential type"""
        try:
            from haystack import connections
            from haystack.backends.solr_backend import SolrSearchBackend

            backend = connections['default'].get_backend()
            if isinstance(backend, SolrSearchBackend):
                # Remove documents referencing the deleted credential_type_id
                # Use query-based deletion to avoid ID conflicts with queue
                queries_to_clean = [
                    f'credential_type_id:{credential_type_id}',
                    f'topic_credential_type_id:{credential_type_id}',
                ]
                
                for query in queries_to_clean:
                    try:
                        backend.conn.delete(q=query)
                        self.stdout.write(f" ... removed Solr docs: {query}")
                    except Exception as e:
                        self.stdout.write(
                            f" ... warning: failed to remove docs for "
                            f"{query}: {e}"
                        )
                
                # Commit changes to ensure cleanup is applied
                try:
                    backend.conn.commit()
                    self.stdout.write(" ... committed Solr changes")
                except Exception as e:
                    self.stdout.write(f" ... warning: commit failed: {e}")
                
                self.stdout.write(" ... search index cleanup completed")
            else:
                self.stdout.write(" ... non-Solr backend, skipping cleanup")
                
        except Exception as e:
            self.stdout.write(
                f" ... warning: search cleanup failed: {str(e)}"
            )
