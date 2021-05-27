from haystack.inputs import Clean, Exact, Raw

from api.v2.search.filters import CredNameFilter, CredNameFilterBuilder


class CredQueryFilterBuilder(CredNameFilterBuilder):

    query_param = "q"


class CredQueryFilter(CredNameFilter):

    query_builder_class = CredQueryFilterBuilder
