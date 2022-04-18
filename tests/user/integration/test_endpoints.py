from django.contrib.auth.hashers import make_password
from django.utils import timezone
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase, APIClient

from faker import Faker

from apps.user.models import UserModel
from services.cpf import CPFLogics

cpf = CPFLogics()
fake = Faker()


class TestUserIntegration(APITestCase):
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

        cls.base_superuser = UserModel.objects.create(
            name=fake.name(),
            email="superuser@email.test",
            password=make_password("superuser"),
            is_active=True,
            date_joined=timezone.now(),
            last_login=timezone.now(),
            is_staff=True,
            is_superuser=True,
            document="06872098112",
        )

        cls.api_logged_user = APIClient()
        cls.base_user_credentials = cls.api_logged_user.credentials(
            HTTP_AUTHORIZATION=f"Token {Token.objects.get_or_create(user=cls.base_user)[0].key}"
        )

        cls.api_logged_superuser = APIClient()
        cls.base_user_credentials = cls.api_logged_superuser.credentials(
            HTTP_AUTHORIZATION=f"Token {Token.objects.get_or_create(user=cls.base_superuser)[0].key}"
        )

        cls.endpoints = {
            "user": "/api/v1/user/",
            "retrieve_user": "/api/v1/user/{}/",
            "login": "/api/v1/login/",
        }

    def test_cant_create_user_with_invalid_email(self):
        payload = {
            "path": self.endpoints["user"],
            "data": {
                "name": fake.name(),
                "document": cpf.force_valid_cpf(),
                "email": "test_invalid_email",
                "password": "test",
            },
        }

        response = self.api_logged_superuser.post(**payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cant_create_user_with_invalid_cpf(self):
        payload = {
            "path": self.endpoints["user"],
            "data": {
                "name": fake.name(),
                "document": "12345678911",
                "email": fake.email(),
                "password": "test",
            },
        }

        response = self.api_logged_superuser.post(**payload)

        assert response.status_code == status.HTTP_400_BAD_REQUEST

    def test_cant_create_user_unauthenticated(self):
        payload = {
            "path": self.endpoints["user"],
            "data": {
                "name": fake.name(),
                "document": cpf.force_valid_cpf(),
                "email": fake.email(),
                "password": "test",
            },
        }

        response = self.api_client.post(**payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_base_user_cant_create_user_authenticated(self):
        payload = {
            "path": self.endpoints["user"],
            "data": {
                "name": fake.name(),
                "document": cpf.force_valid_cpf(),
                "email": fake.email(),
                "password": "test",
            },
        }

        response = self.api_logged_user.post(**payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_can_create_user_authenticated(self):
        payload = {
            "path": self.endpoints["user"],
            "data": {
                "name": fake.name(),
                "document": cpf.force_valid_cpf(),
                "email": fake.email(),
                "password": "test",
            },
        }

        response = self.api_logged_superuser.post(**payload)

        has_token_in_body = "token" in response.data

        assert response.status_code == status.HTTP_201_CREATED
        assert has_token_in_body

    def test_cant_login_with_invalid_password(self):
        payload = {
            "path": self.endpoints["login"],
            "data": {"email": "superuser@email.test", "password": "invalid_password"},
        }

        response = self.api_client.post(**payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_cant_login_with_invalid_email(self):
        payload = {
            "path": self.endpoints["login"],
            "data": {"email": "invalid@email.test", "password": "superuser"},
        }

        response = self.api_client.post(**payload)

        assert response.status_code == status.HTTP_404_NOT_FOUND

    def test_can_login(self):
        payload = {
            "path": self.endpoints["login"],
            "data": {"email": "superuser@email.test", "password": "superuser"},
        }

        response = self.api_client.post(**payload)

        has_token_in_body = "token" in response.data

        assert response.status_code == status.HTTP_200_OK
        assert has_token_in_body

    def test_cant_all_get_unauthenticated(self):
        payload = {"path": self.endpoints["user"]}

        response = self.api_client.get(**payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_cant_retrieve_get_unauthenticated(self):
        payload = {"path": self.endpoints["retrieve_user"].format("1")}
        response = self.api_client.get(**payload)

        assert response.status_code == status.HTTP_401_UNAUTHORIZED

    def test_base_user_can_retrieve_yourself(self):
        payload = {"path": self.endpoints["retrieve_user"].format(self.base_user.id)}
        response = self.api_logged_user.get(**payload)

        assert response.status_code == status.HTTP_200_OK

    def test_base_user_cant_retrieve_another_user(self):
        payload = {
            "path": self.endpoints["retrieve_user"].format(self.base_superuser.id)
        }
        response = self.api_logged_user.get(**payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_base_user_cant_all_get(self):
        payload = {"path": self.endpoints["user"]}
        response = self.api_logged_user.get(**payload)

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_super_user_can_retrieve_yourself(self):
        payload = {
            "path": self.endpoints["retrieve_user"].format(self.base_superuser.id)
        }
        response = self.api_logged_superuser.get(**payload)

        assert response.status_code == status.HTTP_200_OK

    def test_super_user_can_retrieve_another_user(self):
        payload = {"path": self.endpoints["retrieve_user"].format(self.base_user.id)}
        response = self.api_logged_superuser.get(**payload)

        assert response.status_code == status.HTTP_200_OK

    def test_super_user_can_all_get(self):
        payload = {"path": self.endpoints["user"]}
        response = self.api_logged_superuser.get(**payload)

        assert response.status_code == status.HTTP_200_OK
