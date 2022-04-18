from django.test import TestCase
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.viewsets import ModelViewSet

from apps.category.models import CategoryModel
from apps.category.permissions import CategoryPermissions
from apps.category.serializers import CategorySerializer
from apps.category.views import CategoryViewSet
from apps.category.filters import CategoryFilter


class TestCategoryViewSet(TestCase):
    def test_parent(self):
        assert issubclass(CategoryViewSet, ModelViewSet)

    def test_attributes(self):
        self.assertEquals(
            str(CategoryViewSet.queryset),
            str(CategoryModel.objects.order_by("id").filter(is_active=True)),
        )
        self.assertEquals(CategoryViewSet.serializer_class, CategorySerializer)
        self.assertEquals(CategoryViewSet.authentication_classes, [TokenAuthentication])
        self.assertEquals(CategoryViewSet.permission_classes, [CategoryPermissions])
        self.assertEquals(CategoryViewSet.filter_backends, [DjangoFilterBackend])
        self.assertEquals(CategoryViewSet.filterset_class, CategoryFilter)
