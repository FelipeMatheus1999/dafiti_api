from datetime import datetime
from django.test import TestCase

from apps.product.models import ProductModel, product_directory_path

from faker import Faker

from services.base_model import BaseModel

fake = Faker()


class TestProductModel(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.product = ProductModel.objects.create(
            title=fake.name(), description=fake.text(), price=10.0, stock=5
        )

    @staticmethod
    def test_product_is_base_model_instance():
        assert issubclass(ProductModel, BaseModel)

    def test_product_has_information_fields(self):
        self.assertIsInstance(self.product.title, str)
        self.assertIsInstance(self.product.description, str)
        self.assertIsInstance(self.product.price, float)
        self.assertIsInstance(self.product.stock, int)

    def test_product_has_datetime_fields(self):
        self.assertIsInstance(self.product.date_joined, datetime)
        self.assertIsInstance(self.product.date_modified, datetime)

    def test_product_has_bool_fields(self):
        self.assertIsInstance(self.product.is_active, bool)

    def test_dunder_str(self):
        self.assertEquals(str(self.product), self.product.title)

    def test_product_directory_path(self):
        date_now = datetime.now()
        date = date_now.strftime("%d%m%Y_%H:%M:%S")

        file_path = product_directory_path(self.product, "test")
        self.assertEquals(file_path, f"media/{self.product.title}_{date}_test")
