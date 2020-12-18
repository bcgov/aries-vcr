from haystack.inputs import Clean, Exact, Raw

from api.v2.search.filters import (
    CategoryFilter,
    CategoryFilterBuilder
)

from api.v3.search_filters import (
    AutocompleteFilter,
    get_autocomplete_builder
)


class TopicCategoryFilterBuilder(CategoryFilterBuilder):

    query_param = 'topic_category'


class TopicCategoryFilter(CategoryFilter):

    query_builder_class = TopicCategoryFilterBuilder


class TopicQueryFilter(AutocompleteFilter):

    query_builder_class = get_autocomplete_builder(
        ('topic_source_id', 'topic_name', 'topic_address')
    )
