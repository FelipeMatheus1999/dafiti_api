import json

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet

from services.import_export import ExportCSVMixin
from .resources import ProductResource
from .serializers import ProductSerializer
from .models import ProductModel
from .permissions import ProductPermissions
from .filters import ProductFilter


class ProductViewSet(ModelViewSet, ExportCSVMixin):
    queryset = ProductModel.objects.order_by("id").filter(is_active=True)
    serializer_class = ProductSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [ProductPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter
    model_import = ProductModel
    resource = ProductResource

    @method_decorator(cache_page(20, key_prefix="list_products"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)

        serializer = self.get_serializer(page, many=True)
        cache.set("list_products", json.dumps(serializer.data))
        return self.get_paginated_response(serializer.data)

