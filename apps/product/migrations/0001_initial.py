# Generated by Django 4.0.4 on 2022-04-16 10:33

import apps.product.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("category", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="ProductModel",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(auto_now_add=True, verbose_name="Date Joined"),
                ),
                (
                    "date_modified",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Date Modified"
                    ),
                ),
                ("is_active", models.BooleanField(default=True)),
                (
                    "title",
                    models.CharField(max_length=255, verbose_name="Product Title"),
                ),
                ("description", models.TextField(verbose_name="Product Description")),
                (
                    "image",
                    models.FileField(
                        blank=True,
                        null=True,
                        upload_to=apps.product.models.product_directory_path,
                        verbose_name="Product Image",
                    ),
                ),
                ("price", models.FloatField(verbose_name="Product Price")),
                ("stock", models.IntegerField(verbose_name="Product Stock")),
                (
                    "categories",
                    models.ManyToManyField(
                        to="category.categorymodel", verbose_name="Product Categories"
                    ),
                ),
            ],
            options={
                "verbose_name": "Product",
                "verbose_name_plural": "Products",
                "db_table": "product",
            },
        ),
    ]
