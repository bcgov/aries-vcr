import functools
import logging
import operator

from django.conf import settings
from drf_haystack.filters import HaystackFacetFilter, HaystackFilter
from drf_haystack.query import BaseQueryBuilder, FacetQueryBuilder
from haystack.inputs import Clean, Exact, Raw

LOGGER = logging.getLogger(__name__)


class CustomFilter(HaystackFilter):
    pass


class Proximate(Clean):
    """
    Prepare a filter clause matching one or more words, adjusting score according to word proximity
    """

    input_type_name = "contains"
    post_process = False  # don't put AND between terms

    def query_words(self, *parts):
        skip = settings.SEARCH_SKIP_WORDS or ()
        word_len = self.kwargs.get("wordlen", 4)
        for part in parts:
            clean = part.strip()
            if len(clean.strip("_-,.;'\"")) >= word_len and clean.lower() not in skip:
                yield clean

    def prepare(self, query_obj):
        # clean input
        query_string = super(Proximate, self).prepare(query_obj)
        if query_string is not "":
            # match phrase with minimal word movements
            proximity = self.kwargs.get("proximity", 5)
            parts = query_string.split(" ")
            if len(parts) > 1:
                output = '"{}"~{}'.format(query_string, proximity)
            else:
                output = parts[0]
            if "boost" in self.kwargs:
                output = "{}^{}".format(output, self.kwargs["boost"])

            # increase score for any individual term
            if self.kwargs.get("any") and len(parts) > 1:
                words = list(self.query_words(*parts))
                if words:
                    output = " OR ".join([output, *words])
        else:
            output = query_string
        return output


def get_autocomplete_builder(attr_names):
    class AutocompleteFilterBuilder(BaseQueryBuilder):
        query_param = "q"

        def build_name_query(self, term):
            SQ = self.view.query_object
            match_any = not settings.SEARCH_TERMS_EXCLUSIVE

            query = None
            assert len(attr_names) > 0
            for attr_name in attr_names:
                sq_precise_args = {
                    f"{attr_name}_precise": Proximate(term, boost=10, any=match_any)
                }
                sq_suggest_args = {f"{attr_name}_suggest": Proximate(term)}
                if not query:
                    query = SQ(**sq_suggest_args) | SQ(**sq_precise_args)
                else:
                    query |= SQ(**sq_suggest_args) | SQ(**sq_precise_args)

            return query

        def build_query(self, **filters):
            inclusions = []
            exclusions = None
            if self.query_param in filters:
                for qval in filters[self.query_param]:
                    if len(qval):
                        inclusions.append(self.build_name_query(qval))
            inclusions = (
                functools.reduce(operator.and_, inclusions) if inclusions else None
            )
            return inclusions, exclusions

    return AutocompleteFilterBuilder


class AutocompleteFilter(CustomFilter):
    """
    Apply name autocomplete filter to credential search
    """

    query_builder_class = get_autocomplete_builder(
        ("name_text", "address_civic_address", "topic_source_id", "topic_name")
    )


class StatusFilterBuilder(BaseQueryBuilder):
    def build_query(self, **filters):
        inclusions = {}
        exclusions = None
        SQ = self.view.query_object
        filter_fields_map = getattr(
            self.view.serializer_class.Meta, "filter_fields_map", ()
        )

        # For every parameter passed in the request
        for qname, qvals in filters.items():
            for qval in qvals:
                # Check if we track this filter type in the serializer
                # in `filter_fields_map` tuple
                if qname in filter_fields_map:
                    mapped_index_attributes = filter_fields_map[qname]
                    attr_inclusions = {}
                    # Construct an OR clause for this filter across all of the
                    # mapped index attributes
                    for mapped_attr in mapped_index_attributes:
                        attr_inclusions[mapped_attr] = SQ(**{mapped_attr: Exact(qval)})
                    attr_inclusions = (
                        functools.reduce(operator.or_, attr_inclusions.values())
                        if attr_inclusions
                        else None
                    )
                    # Add this sub OR clause to the top-level set of AND clauses
                    inclusions[mapped_attr] = attr_inclusions

        inclusions = (
            functools.reduce(operator.and_, inclusions.values()) if inclusions else None
        )

        return inclusions, exclusions


class StatusFilter(CustomFilter):
    """
    Apply boolean filter flags
    """

    query_builder_class = StatusFilterBuilder
