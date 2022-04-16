from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from faker import Faker

from apps.category.models import CategoryModel
from apps.user.models import UserModel
from services.cpf import CPFLogics

cpf = CPFLogics()
fake = Faker()


class TestProductIntegration(APITestCase):
    @classmethod
    def setUpTestData(cls):
        cls.api_client = APIClient()

        cls.base_user = UserModel.objects.create(
            name=fake.name(),
            email="baseuser@email.test",
            password=make_password("baseuser"),
            is_active=True,
            date_joined=timezone.now(),
            last_login=timezone.now(),
            document="90078144191",
        )

        cls.base_category = CategoryModel.objects.create(
            name=fake.name()
        )

        cls.api_logged_user = APIClient()
        cls.base_user_credentials = cls.api_logged_user.credentials(HTTP_AUTHORIZATION=f"Token {Token.objects.get_or_create(user=cls.base_user)[0].key}")

        cls.endpoints = {
            "category": "/api/v1/category/",
            "retrieve_category": "/api/v1/category/{}/"
        }

    def test_cant_get_category_unauthenticated(self):
        payload = {
            "path": self.endpoints["category"]
        }

        response = self.api_client.get(**payload)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_get_category_authenticated(self):
        payload = {
            "path": self.endpoints["category"]
        }

        response = self.api_logged_user.get(**payload)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_cant_create_category_unauthenticated(self):
        payload = {
            "path": self.endpoints["category"]
        }

        response = self.api_client.post(**payload)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_category_authenticated(self):
        payload = {
            "path": self.endpoints["category"],
            "data": {
                "name": "Test"
            }
        }

        response = self.api_logged_user.post(**payload)

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_cant_update_category_unauthenticated(self):
        payload = {
            "path": self.endpoints["retrieve_category"].format("1"),
            "data": {
                "name": "Test"
            }
        }

        response = self.api_client.patch(**payload)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_cant_update_category_authenticated_with_existent_name(self):
        CategoryModel.objects.create(
            name="TestRepeat"
        )

        payload = {
            "path": self.endpoints["retrieve_category"].format(self.base_category.id),
            "data": {
                "name": "TestRepeat"
            }
        }

        response = self.api_logged_user.patch(**payload)

        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_can_update_category_authenticated(self):
        payload = {
            "path": self.endpoints["retrieve_category"].format(self.base_category.id),
            "data": {
                "name": "Test Can Update"
            }
        }

        response = self.api_logged_user.patch(**payload)

        self.assertEquals(response.status_code, status.HTTP_200_OK)
