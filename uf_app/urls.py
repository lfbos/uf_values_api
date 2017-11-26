from django.conf.urls import url

from uf_app.api.views import uf_price_api_view, UFValueViewSet

urlpatterns = [
    url(r'^uf/list/$', UFValueViewSet.as_view({'get': 'list'})),
    url(r'^uf/price/$', uf_price_api_view)
]
