from django.test import TestCase
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from apps.product.models import ProductModel
from apps.product.permissions import ProductPermissions
from apps.product.resources import ProductResource
from apps.product.serializers import ProductSerializer
from apps.product.views import ProductViewSet


class TestProductViewSet(TestCase):
    def test_parent(self):
        assert issubclass(ProductViewSet, ModelViewSet)

    def test_attributes(self):
        self.assertEquals(
            str(ProductViewSet.queryset),
            str(ProductModel.objects.order_by("id").filter(is_active=True)),
        )
        self.assertEquals(ProductViewSet.serializer_class, ProductSerializer)
        self.assertEquals(ProductViewSet.authentication_classes, [TokenAuthentication])
        self.assertEquals(ProductViewSet.permission_classes, [ProductPermissions])
        self.assertEquals(ProductViewSet.filter_backends, [DjangoFilterBackend])
        self.assertEquals(ProductViewSet.model_import, ProductModel)
        self.assertEquals(ProductViewSet.resource, ProductResource)
