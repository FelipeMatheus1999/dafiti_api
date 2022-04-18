from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from faker import Faker

from apps.product.models import ProductModel
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

        cls.base_product = ProductModel.objects.create(
            title=fake.name(),
            description=fake.text(),
            price=10.0,
            stock=50,
        )

        cls.api_logged_user = APIClient()
        cls.base_user_credentials = cls.api_logged_user.credentials(
            HTTP_AUTHORIZATION=f"Token {Token.objects.get_or_create(user=cls.base_user)[0].key}"
        )

        cls.endpoints = {
            "product": "/api/v1/product/",
            "retrieve_product": "/api/v1/product/{}/",
        }

    def test_cant_get_products_unauthenticated(self):
        payload = {"path": self.endpoints["product"]}
        response = self.api_client.get(**payload)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_get_products_authenticated(self):
        payload = {"path": self.endpoints["product"]}
        response = self.api_logged_user.get(**payload)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_can_get_page_products_authenticated(self):
        payload = {"path": self.endpoints["product"] + "?page=1"}
        response = self.api_logged_user.get(**payload)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_can_get_retrieve_products_authenticated(self):
        payload = {"path": self.endpoints["product"].format(self.base_product.id)}
        response = self.api_logged_user.get(**payload)

        self.assertEquals(response.status_code, status.HTTP_200_OK)

    def test_cant_create_products_unauthenticated(self):

        payload = {"path": self.endpoints["product"]}
        response = self.api_client.post(**payload)

        self.assertEquals(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_can_create_products_authenticated(self):
        payload = {
            "path": self.endpoints["product"],
            "data": {
                "title": "Yellow Short",
                "description": "test",
                "price": 145,
                "stock": 14,
                "categories": [{"name": "Summer"}, {"name": "Ice"}],
            },
        }
        response = self.api_logged_user.post(**payload, format="json")

        self.assertEquals(response.status_code, status.HTTP_201_CREATED)

    def test_can_update_products_authenticated(self):
        payload = {
            "path": self.endpoints["retrieve_product"].format(self.base_product.id),
            "data": {
                "categories": [{"name": "Summer"}, {"name": "Ice"}],
            },
        }
        response = self.api_logged_user.patch(**payload, format="json")

        self.assertEquals(response.status_code, status.HTTP_200_OK)
