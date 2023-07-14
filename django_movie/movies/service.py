from django_filters import rest_framework as filters
from rest_framework.response import Response

from .models import Movie
from rest_framework.pagination import PageNumberPagination


def get_client_ip(request):
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class FilterInFilter(filters.BaseInFilter, filters.CharFilter):
    """
    filters.BaseInFilter: для выполнения фильтрации по оператору in для поля 
    filters.CharFilter: Для фильтрации на основе символьных значении
    """
    pass


class MovieFilter(filters.FilterSet):
    genres = FilterInFilter(field_name='genres__name', lookup_expr='in')
    year = filters.RangeFilter()

    class Meta:
        model = Movie
        fields = ('genres', 'year')

class Pagination(PageNumberPagination):
    page_size = 4
    max_page_size = 1000

    def get_paginated_response(self, data):
        return Response({
            'link': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'result': data
        })