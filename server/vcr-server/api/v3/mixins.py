# Taken from https://stackoverflow.com/a/38462137/338724

from django.shortcuts import get_object_or_404
from django.db.models import Q

import operator
from functools import reduce


class MultipleFieldLookupMixin(object):
    def get_object(self):
        queryset = self.get_queryset()  # Get the base queryset
        queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        q = reduce(operator.and_, (Q(x) for x in filter.items()))
        return get_object_or_404(queryset, q)
