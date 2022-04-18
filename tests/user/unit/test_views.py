from django.test import TestCase
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.authentication import TokenAuthentication
from rest_framework.throttling import UserRateThrottle
from rest_framework.viewsets import ModelViewSet, ViewSet

from apps.user.filters import UserFilter
from apps.user.models import UserModel
from apps.user.permissions import UserPermissions
from apps.user.serializers import UserSerializer
from apps.user.views import UserViewSet, UserLoginViewSet


class TestUserViewSet(TestCase):
    def test_parent(self):
        assert issubclass(UserViewSet, ModelViewSet)

    def test_attributes(self):
        self.assertEquals(
            str(UserViewSet.queryset),
            str(UserModel.objects.order_by("id").filter(is_active=True)),
        )
        self.assertEquals(UserViewSet.serializer_class, UserSerializer)
        self.assertEquals(UserViewSet.authentication_classes, [TokenAuthentication])
        self.assertEquals(UserViewSet.permission_classes, [UserPermissions])
        self.assertEquals(UserViewSet.throttle_classes, [UserRateThrottle])
        self.assertEquals(UserViewSet.filter_backends, [DjangoFilterBackend])
        self.assertEquals(UserViewSet.filterset_class, UserFilter)


class TestUserLoginViewSet(TestCase):
    def test_parent(self):
        assert issubclass(UserLoginViewSet, ViewSet)

    def test_attributes(self):
        self.assertEquals(str(UserLoginViewSet.queryset), str(UserModel.objects.all()))
