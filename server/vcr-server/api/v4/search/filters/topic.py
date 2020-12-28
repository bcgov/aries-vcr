from haystack.inputs import Clean, Exact, Raw
from drf_haystack.query import BaseQueryBuilder

from api.v2.search.filters import (
    CategoryFilter,
    CategoryFilterBuilder,
    ExactFilter,
    ExactFilterBuilder,
    StatusFilter,
    StatusFilterBuilder
)

from api.v3.search_filters import (
    AutocompleteFilter,
    get_autocomplete_builder
)

filter_display_names = ['category', 'issuer_id',
                        'type_id', 'credential_type_id', 'inactive', 'revoked']


class FilterBuilderBase(BaseQueryBuilder):

    def format_filters(self, **filters):
        for fname, fval in filters.copy().items():
            partition = ':'
            parts = fname.split(partition)
            if parts[0] in filter_display_names:
                filters['topic_' + partition.join(parts)] = fval
                del filters[fname]
        return filters


class TopicCategoryFilterBuilder(FilterBuilderBase, CategoryFilterBuilder):

    query_param = 'topic_category'

    def build_query(self, **filters):
        return super(TopicCategoryFilterBuilder, self).build_query(**self.format_filters(**filters))


class TopicExactFilterBuilder(FilterBuilderBase, ExactFilterBuilder):

    def build_query(self, **filters):
        return super(TopicExactFilterBuilder, self).build_query(**self.format_filters(**filters))


class TopicStatusFilterBuilder(FilterBuilderBase, StatusFilterBuilder):

    def build_query(self, **filters):
        return super(TopicStatusFilterBuilder, self).build_query(**self.format_filters(**filters))


class TopicCategoryFilter(CategoryFilter):

    query_builder_class = TopicCategoryFilterBuilder


class TopicExactFilter(ExactFilter):

    query_builder_class = TopicExactFilterBuilder


class TopicStatusFilter(StatusFilter):

    query_builder_class = TopicStatusFilterBuilder


class TopicQueryFilter(AutocompleteFilter):

    query_builder_class = get_autocomplete_builder(
        ('topic_source_id', 'topic_name', 'topic_address')
    )
