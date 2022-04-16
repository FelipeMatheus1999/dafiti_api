from datetime import datetime

from django.db import models
from services.base_model import BaseModel
from apps.category.models import CategoryModel
from django.utils.translation import gettext_lazy as _


def product_directory_path(instance, filename):
    date_now = datetime.now()
    date = date_now.strftime("%d%m%Y_%H:%M:%S")

    return f"media/{instance.title}_{date}_{filename}"


class ProductModel(BaseModel):
    title = models.CharField(max_length=255, verbose_name=_("Product Title"))
    description = models.TextField(verbose_name=_("Product Description"))
    image = models.FileField(upload_to=product_directory_path, null=True, blank=True, verbose_name=_("Product Image"))
    price = models.FloatField(verbose_name=_("Product Price"))
    stock = models.IntegerField(verbose_name=_("Product Stock"))

    categories = models.ManyToManyField(CategoryModel, verbose_name=_("Product Categories"))

    def __str__(self):
        return self.title

    class Meta:
        db_table = "product"
        verbose_name = _("Product")
        verbose_name_plural = _("Products")
