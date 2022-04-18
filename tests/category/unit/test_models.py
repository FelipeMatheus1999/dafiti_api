from datetime import datetime
from django.test import TestCase

from apps.category.models import CategoryModel

from faker import Faker

from services.base_model import BaseModel

fake = Faker()


class TestCategoryModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.category = CategoryModel.objects.create(name=fake.name())

    @staticmethod
    def test_category_is_base_model_instance():
        assert issubclass(CategoryModel, BaseModel)

    def test_category_has_information_fields(self):
        self.assertIsInstance(self.category.name, str)

    def test_category_has_datetime_fields(self):
        self.assertIsInstance(self.category.date_joined, datetime)
        self.assertIsInstance(self.category.date_modified, datetime)

    def test_category_has_bool_fields(self):
        self.assertIsInstance(self.category.is_active, bool)

    def test_dunder_str(self):
        self.assertEquals(str(self.category), self.category.name)
