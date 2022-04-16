import random
from faker import Faker
from django.core.management.base import BaseCommand

from apps.category.models import CategoryModel
from apps.product.models import ProductModel


class Command(BaseCommand):
    def handle(self, *_, **options):
        fake = Faker()
        adjective_list = ["Blue", "Yellow", "Black", "Green", "Red"]
        product_list = ["Pants", "Shorts", "Dress", "Shoes", "Shirt"]
        categories = ["Teen", "Classic", "Vintage", "Summer", "Old School"]
        categories_id = [CategoryModel.objects.get_or_create(name=category)[0] for category in categories]

        for _ in range(100):
            fields = {
                "title": f"{adjective_list[random.randrange(0, len(adjective_list))]} {product_list[random.randrange(0, len(product_list))]}",
                "description": fake.text(),
                "price": float(random.randrange(100, 200)),
                "stock": random.randrange(10, 100),
            }
            product = ProductModel.objects.create(**fields)

            product_categories = [categories_id[random.randrange(0, len(categories_id))]]
            product.categories.set(product_categories)

        self.stdout.write(f"100 products was created")
