import django_filters
from django.utils.translation import ugettext as _
from django_filters import rest_framework as filters
from rest_framework import viewsets, status
from rest_framework.decorators import api_view
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

from uf_app.api.serializers import UFValueSerializer, UFPriceSerializer
from uf_app.models import UFValue
from uf_app.utils import pesos_to_uf


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
    value = request.query_params.get('value')
    date = request.query_params.get('date')

    if value is None and date is None:
        return Response({
            "error": _("You must pass a value (chilean pesos) and a date as parameters.")
        }, status=status.HTTP_400_BAD_REQUEST)

    data = {
        'value': value,
        'date': date
    }

    serializer = UFPriceSerializer(data=data)
    serializer.is_valid(raise_exception=True)

    data = serializer.validated_data
    uf_value = get_object_or_404(UFValue, date=data.get('date'))

    data.update({
        'price': pesos_to_uf(data.get('value'), uf_value.value)
    })

    return Response(data, status=status.HTTP_200_OK)
