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
        
        # Reindex remaining credentials that might have cached references
        self.stdout.write("Reindexing remaining credentials ...")
        self._reindex_remaining_credentials()
        
        # Final facet refresh to ensure UI shows correct data
        self.stdout.write("Performing final facet refresh ...")
        self._force_facet_refresh()
        
        self.stdout.write("Done.")

        processing_time = time.perf_counter() - start_time
        self.stdout.write(f"Processing time: {processing_time} sec")

    def _clear_topic_caches(self, credential_type_id):
        """Clear Topic caches before deletion to prevent stale indexing"""
        try:
            from api.v2.models.Credential import Credential
            from api.v2.models.Topic import Topic
            from django.core.cache import cache
            from django.db import connection, reset_queries

            # Find all topics that have credentials of this type
            topic_ids = set(Credential.objects.filter(
                credential_type_id=credential_type_id
            ).values_list('topic_id', flat=True))
            
            # Store affected topic IDs for later reindexing
            self._affected_topic_ids = topic_ids
            
            self.stdout.write(
                f" ... clearing caches for {len(topic_ids)} affected topics"
            )
            self.stdout.write(
                " ... clearing all model-level caches as safety measure"
            )
            
            # Clear Topic-level caches for ALL topics
            for topic in Topic.objects.all():
                topic._active_cred_ids = None
                topic._active_cred_type_ids = None
            
            # Clear Credential-level caches for ALL credentials
            self.stdout.write(" ... clearing credential-level caches")
            for credential in Credential.objects.all():
                credential._cache = None
            
            # Clear Django ORM internal caches
            self.stdout.write(" ... clearing ORM and connection caches")
            
            # Clear connection-level caches
            if hasattr(connection, 'queries_log'):
                connection.queries_log.clear()
            if hasattr(connection, 'queries'):
                connection.queries.clear()
            
            # Reset queries tracking
            reset_queries()
            
            # Clear any Django cache framework caches
            cache.clear()
            
            # Force connection reset to clear connection-level state
            connection.close()
                    
            self.stdout.write(
                " ... all caches cleared including ORM and connection level"
            )
            
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
                
                # Aggressive Solr cache clearing for facets
                self.stdout.write(" ... clearing Solr facet caches")
                
                # First commit changes
                backend.conn.commit()
                
                # Force reload of Solr cores to clear all caches
                try:
                    # Clear facet cache specifically
                    backend.conn._send_request('get', '/admin/cores', params={
                        'action': 'RELOAD',
                        'core': backend.conn.decoder.collection
                    })
                    self.stdout.write(" ... Solr core reloaded")
                except Exception as reload_error:
                    self.stdout.write(
                        f" ... core reload failed: {reload_error}"
                    )
                
                # Optimize to consolidate segments and refresh caches
                backend.conn.optimize(waitSearcher=True)
                
                # Additional commit to ensure all changes are flushed
                backend.conn.commit(waitSearcher=True)
                
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
                " ... manually reindexing affected topics"
            )
            
            # Use the stored affected topic IDs if available
            affected_topic_ids = getattr(self, '_affected_topic_ids', set())
            
            # Also include topics that had recent activity as fallback
            recent_topics = Topic.objects.filter(
                update_timestamp__gte=timezone.now() - timedelta(hours=24)
            ).values_list('id', flat=True)
            
            # Combine both sets
            all_topic_ids = affected_topic_ids.union(set(recent_topics))
            
            # Get the actual topic objects for reindexing
            topics_to_update = Topic.objects.filter(
                id__in=all_topic_ids
            )
            
            updated_count = 0
            
            for topic in topics_to_update:
                try:
                    # Clear cached values to force fresh computation
                    topic._active_cred_ids = None
                    topic._active_cred_type_ids = None
                    
                    # Manual signal processing like reprocess_credentials does
                    # This ensures complete reindexing similar to update_index
                    signals.post_save.send(
                        sender=Topic, instance=topic, using=DEFAULT_DB_ALIAS
                    )
                    
                    updated_count += 1
                    
                except Exception as e:
                    self.stdout.write(
                        f" ... warning: failed to reindex topic "
                        f"{topic.pk}: {e}"
                    )
            
            if updated_count > 0:
                self.stdout.write(
                    f" ... reindexed {updated_count} affected topics"
                )
            else:
                self.stdout.write(" ... no topics required reindexing")
            
        except Exception as e:
            self.stdout.write(
                f" ... warning: topic reindexing failed: {str(e)}"
            )

    def _reindex_remaining_credentials(self):
        """Reindex remaining credentials to clear any cached references"""
        try:
            from api.v2.models.Credential import Credential
            from django.db import DEFAULT_DB_ALIAS
            from django.db.models import signals

            self.stdout.write(" ... reindexing remaining credentials")
            
            # Get affected topics if available
            affected_topic_ids = getattr(self, '_affected_topic_ids', set())
            
            if affected_topic_ids:
                # Only reindex credentials for affected topics
                remaining_credentials = Credential.objects.filter(
                    topic_id__in=affected_topic_ids
                ).select_related('topic', 'credential_type')
                
                count = remaining_credentials.count()
                if count > 0:
                    self.stdout.write(
                        f" ... reindexing {count} credentials "
                        f"from affected topics"
                    )
                    
                    for credential in remaining_credentials:
                        try:
                            # Clear credential cache
                            credential._cache = None
                            
                            # Manual signal processing for reindexing
                            signals.post_save.send(
                                sender=Credential,
                                instance=credential,
                                using=DEFAULT_DB_ALIAS
                            )
                        except Exception as e:
                            self.stdout.write(
                                f" ... warning: failed to reindex "
                                f"credential {credential.pk}: {e}"
                            )
                else:
                    self.stdout.write(
                        " ... no remaining credentials to reindex"
                    )
            else:
                self.stdout.write(
                    " ... no affected topics found for reindexing"
                )
                    
        except Exception as e:
            self.stdout.write(
                f" ... warning: credential reindexing failed: {str(e)}"
            )

    def _force_facet_refresh(self):
        """Force a complete facet refresh by rebuilding the search index"""
        try:
            from haystack import connections
            from haystack.backends.solr_backend import SolrSearchBackend

            self.stdout.write(" ... forcing complete facet refresh")
            
            backend = connections['default'].get_backend()
            if isinstance(backend, SolrSearchBackend):
                # Method 1: Direct Solr operations
                try:
                    # Clear all cached queries
                    backend.clear()
                    
                    # Force a new searcher to be opened
                    backend.conn.commit(waitSearcher=True, expungeDeletes=True)
                    
                    # Optimize with full merge to ensure clean state
                    backend.conn.optimize(waitSearcher=True, maxSegments=1)
                    
                    self.stdout.write(" ... Solr facet caches cleared")
                except Exception as solr_error:
                    self.stdout.write(
                        f" ... Solr facet clear failed: {solr_error}"
                    )
                
                # Method 2: Trigger a quick reindex of a small set to refresh
                try:
                    from api.v2.models.CredentialType import CredentialType

                    # Get a small sample of remaining credential types
                    remaining_types = CredentialType.objects.all()[:5]
                    
                    if remaining_types:
                        self.stdout.write(
                            f" ... refreshing {len(remaining_types)} "
                            f"credential types to update facets"
                        )
                        
                        for cred_type in remaining_types:
                            try:
                                # Force reindexing by updating timestamp
                                cred_type.save(
                                    update_fields=['update_timestamp']
                                )
                            except Exception as save_error:
                                self.stdout.write(
                                    f" ... refresh failed for type "
                                    f"{cred_type.pk}: {save_error}"
                                )
                        
                        # Final commit after refresh
                        backend.conn.commit(waitSearcher=True)
                        
                    self.stdout.write(" ... facet refresh completed")
                except Exception as refresh_error:
                    self.stdout.write(
                        f" ... facet refresh failed: {refresh_error}"
                    )
            else:
                self.stdout.write(
                    " ... non-Solr backend, skipping facet refresh"
                )
                
        except Exception as e:
            self.stdout.write(
                f" ... warning: facet refresh failed: {str(e)}"
            )
