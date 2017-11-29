import django_filters
from decimal import Decimal
from django.utils.translation import ugettext as _
from django_filters import rest_framework as filters
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework.exceptions import APIException
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from uf_app.api.serializers import UFValueSerializer
from uf_app.models import UFValue
from uf_app.utils import string_to_date, pesos_to_uf
from uf_app.validators import is_valid_float, is_valid_date

INVALID_DATE_ERROR_MESSAGE = _('Date format invalid must be yyyymmdd (year, month, day)')
INVALID_VALUE_ERROR_MESSAGE = _('Value must be valid float')


class UFValuePagination(PageNumberPagination):
    page_size_query_param = 'page_size'
    page_size = 365


class UFValueFilter(filters.FilterSet):
    year = django_filters.CharFilter(name='date', lookup_expr='year')

    class Meta:
        model = UFValue
        fields = ('value', 'date', 'year')


class UFValueViewSet(viewsets.ReadOnlyModelViewSet):
    serializer_class = UFValueSerializer
    queryset = UFValue.objects.all()
    filter_class = UFValueFilter
    pagination_class = UFValuePagination


# This view could use cache
@api_view(['GET'])
def uf_price_api_view(request):
    value_string = request.query_params.get('value')
    date_string = request.query_params.get('date')

    if not value_string or not date_string:
        return Response({})

    if not is_valid_float(value_string):
        raise APIException(INVALID_VALUE_ERROR_MESSAGE)

    if not is_valid_date(date_string):
        raise APIException(INVALID_DATE_ERROR_MESSAGE)

    date = string_to_date(date_string)
    value = Decimal(value_string)

    uf_value = get_object_or_404(UFValue, date=date)

    price = pesos_to_uf(value, uf_value.value)

    return Response({
        "price": price,
        "value": value,
        "date": date.to_date_string()
    })
