# DEPRECATED: this should not be used in new code and will be removed imminently
from api.v3.search_filters import AutocompleteFilter as V3AutocompleteFilter
from api.v3.search_filters import get_autocomplete_builder


class AutocompleteFilter(V3AutocompleteFilter):
    """
    Apply name autocomplete filter to credential search
    """

    query_builder_class = get_autocomplete_builder(
        ("name_text", "address_civic_address", "topic_source_id", "topic_name")
    )
