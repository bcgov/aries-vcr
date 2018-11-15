import functools
import logging
import operator

from drf_haystack.query import BaseQueryBuilder, FilterQueryBuilder
from drf_haystack.filters import HaystackFilter
from haystack.inputs import Clean, Exact, Raw

LOGGER = logging.getLogger(__name__)


class Proximate(Clean):
    """
    Prepare a filter clause matching one or more words, adjusting score according to word proximity
    """
    input_type_name = 'contains'
    post_process = False # don't put AND between terms

    def prepare(self, query_obj):
        # clean input
        query_string = super(Proximate, self).prepare(query_obj)
        if query_string is not '':
            # match phrase with minimal word movements
            proximity = self.kwargs.get('proximity', 100)
            parts = query_string.split(' ')
            if len(parts) > 1:
                output = '"{}"~{}'.format(query_string, proximity)
            else:
                output = parts[0]
            if 'boost' in self.kwargs:
                output = '{}^{}'.format(output, self.kwargs['boost'])
            # increase score for any individual term
            if len(parts) > 1 and self.kwargs.get('any'):
                output = ' OR '.join([output, *parts])
        else:
            output = query_string
        return output


class AutocompleteFilterBuilder(BaseQueryBuilder):
    query_param = 'q'

    def build_name_query(self, term):
        SQ = self.view.query_object
        return SQ(name_suggest=Proximate(term)) \
               | SQ(name_precise=Proximate(term, boost=10, any=True))

    def build_query(self, **filters):
        inclusions = []
        exclusions = None
        SQ = self.view.query_object
        if self.query_param in filters:
            for qval in filters[self.query_param]:
                inclusions.append(self.build_name_query(qval))
        inclusions = functools.reduce(operator.and_, inclusions) if inclusions else None
        return inclusions, exclusions


class AutocompleteFilter(HaystackFilter):
    """
    Apply name autocomplete filter to credential search
    """
    query_builder_class = AutocompleteFilterBuilder


class CategoryFilterBuilder(BaseQueryBuilder):
    query_param = 'category'

    def build_query(self, **filters):
        inclusions = []
        exclusions = []
        SQ = self.view.query_object
        for qname, qvals in filters.items():
            category = None
            by_value = False
            negate = False
            if ':' in qname:
                parts = qname.split(':', 2)
                if parts[0] == self.query_param:
                    category = parts[1]
                    if '__' in category:
                        parts = category.split('__', 2)
                        category = parts[0]
                        if parts[1] == 'not':
                            negate = True
                        elif parts[1] != 'exact':
                            continue
            else:
                if '__' in qname:
                    parts = qname.split('__', 2)
                    qname = parts[0]
                    if parts[1] == 'not':
                        negate = True
                    elif parts[1] != 'exact':
                        continue
                if qname == self.query_param:
                    by_value = True
            if not category and not by_value:
                continue
            fvals = []
            for qv in qvals:
                if not qv:
                    continue
                if by_value:
                    if '::' not in qv:
                        continue
                    filt = Exact(qv)
                else:
                    filt = Exact('{}::{}'.format(category, qv))
                fvals.append(filt)
            if fvals:
                clauses = (SQ(**{self.query_param: fval}) for fval in fvals)
                if negate:
                    exclusions.extend(clauses)
                else:
                    inclusions.extend(clauses)
        inclusions = functools.reduce(operator.or_, inclusions) if inclusions else None
        exclusions = functools.reduce(operator.or_, exclusions) if exclusions else None
        return inclusions, exclusions


class CategoryFilter(HaystackFilter):
    """
    Apply category filters to credential search
    """
    query_builder_class = CategoryFilterBuilder


class CredNameFilterBuilder(AutocompleteFilterBuilder):
    """
    Augment autocomplete filter with matching on the related topic source ID
    """
    query_param = 'name'

    def build_name_query(self, term):
        SQ = self.view.query_object
        filter = super(CredNameFilterBuilder, self).build_name_query(term) \
               | (SQ(source_id=Exact(term)) & SQ(name=Raw('*')))
        return filter


class CredNameFilter(AutocompleteFilter):
    """
    Apply autocomplete filter
    """
    query_builder_class = CredNameFilterBuilder


class StatusFilterBuilder(BaseQueryBuilder):
    def build_query(self, **filters):
        inclusions = {}
        exclusions = None
        SQ = self.view.query_object
        status_fields = getattr(self.view.serializer_class.Meta, 'status_fields', {})
        for qname, qval in status_fields.items():
            if qval and qval != 'any':
                inclusions[qname] = SQ(**{qname: Exact(qval)})
        for qname, qvals in filters.items():
            if qname not in status_fields:
                continue
            for qval in qvals:
                if qval and qval != 'any':
                    inclusions[qname] = SQ(**{qname: Exact(qval)})
        inclusions = functools.reduce(operator.and_, inclusions.values()) if inclusions else None
        return inclusions, exclusions


class StatusFilter(HaystackFilter):
    """
    Apply boolean filter flags
    """
    query_builder_class = StatusFilterBuilder
