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


class AutocompleteFilterBuilder(BaseQueryBuilder):
    query_param = "q"

    def build_name_query(self, term):
        SQ = self.view.query_object
        match_any = not settings.SEARCH_TERMS_EXCLUSIVE
        return SQ(name_text_suggest=Proximate(term)) | SQ(
            name_text_precise=Proximate(term, boost=10, any=match_any)
        )

    def build_query(self, **filters):
        inclusions = []
        exclusions = None
        if self.query_param in filters:
            for qval in filters[self.query_param]:
                if len(qval):
                    inclusions.append(self.build_name_query(qval))
        inclusions = functools.reduce(operator.and_, inclusions) if inclusions else None
        return inclusions, exclusions


class AutocompleteFilter(CustomFilter):
    """
    Apply name autocomplete filter to credential search
    """

    query_builder_class = AutocompleteFilterBuilder
