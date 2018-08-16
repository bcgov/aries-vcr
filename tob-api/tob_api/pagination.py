from collections import OrderedDict

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class EnhancedPageNumberPagination(PageNumberPagination):
    page_size = 10

    def get_paginated_response(self, data):
        return Response(
            OrderedDict(
                [
                    ("total", self.page.paginator.count),
                    ("page_size", self.page_size),
                    ("page", self.page.number),
                    ("first_index", self.page.start_index()),
                    ("last_index", self.page.end_index()),
                    ("next", self.get_next_link()),
                    ("previous", self.get_previous_link()),
                    ("results", data),
                ]
            )
        )
