from datetime import datetime

from django.contrib.auth.hashers import make_password
from django.test import TestCase
from django.utils import timezone

from apps.user.models import UserModel

from faker import Faker

fake = Faker()


class TestUserModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.base_user = UserModel.objects.create(
            name=fake.name(),
            email=fake.unique.email(),
            password=make_password(fake.name()),
            last_login=timezone.now(),
            document="00000000000",
        )
        cls.super_user = UserModel.objects.create_superuser(
            name=fake.name(),
            email=fake.unique.email(),
            password=make_password(fake.name()),
        )
        cls.user = UserModel.objects.create_user(
            name=fake.name(),
            email=fake.unique.email(),
            password=make_password(fake.name()),
        )

    def test_final_user_model_hasnt_default_fields(self):
        self.assertIsInstance(self.base_user.username, type(None))
        self.assertIsInstance(self.base_user.user_permissions, type(None))
        self.assertIsInstance(self.base_user.first_name, type(None))
        self.assertIsInstance(self.base_user.last_name, type(None))
        self.assertIsInstance(self.base_user.groups, type(None))

    def test_final_user_model_has_information_fields(self):
        self.assertIsInstance(self.base_user.name, str)
        self.assertIsInstance(self.base_user.email, str)
        self.assertIsInstance(self.base_user.password, str)
        self.assertIsInstance(self.base_user.is_active, bool)
        self.assertIsInstance(self.base_user.document, str)
        self.assertIsInstance(self.base_user.is_superuser, bool)
        self.assertIsInstance(self.base_user.is_staff, bool)

    def test_final_user_model_has_datetime_fields(self):
        self.assertIsInstance(self.base_user.date_joined, datetime)
        self.assertIsInstance(self.base_user.last_login, datetime)

    def test_dunder_str(self):
        self.assertEquals(str(self.base_user), self.base_user.name)

    def test_manager_create_super_user(self):
        self.assertEquals(self.super_user.is_staff, True)
        self.assertEquals(self.super_user.is_superuser, True)

    def test_manager_create_user(self):
        self.assertEquals(self.user.is_staff, False)
        self.assertEquals(self.user.is_superuser, False)

    def test_manager_cant_create_user_without_email(self):
        self.assertRaises(ValueError, UserModel.objects.create_user, False)
