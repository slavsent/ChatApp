from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response


class UserListPaginator(PageNumberPagination):
    # TODO Пофиксить выдачу limit в пагинаторе
    page_size_query_param = 'page_size'

    def __init__(self, page_size=10, *args, **kwargs):
        self.page_size = page_size
        super().__init__(*args, **kwargs)

    def get_paginated_response(self, data):
        return Response({
            'count': self.page.paginator.count,
            'next': self.get_next_link(),
            'previous': self.get_previous_link(),
            'limit': self.page_size,
            'results': data
        })
