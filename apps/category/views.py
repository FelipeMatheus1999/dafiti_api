import json

from django.core.cache import cache
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_headers
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .serializers import CategorySerializer
from .models import CategoryModel
from .permissions import CategoryPermissions
from .filters import CategoryFilter


class CategoryViewSet(ModelViewSet):
    queryset = CategoryModel.objects.order_by("id").filter(is_active=True)
    serializer_class = CategorySerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [CategoryPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CategoryFilter

    @method_decorator(cache_page(20, key_prefix="list_category"))
    @method_decorator(vary_on_headers("Authorization"))
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        page = self.paginate_queryset(queryset)
        serializer = self.get_serializer(page, many=True)
        cache.set("list_category", json.dumps(serializer.data))
        return self.get_paginated_response(serializer.data)
