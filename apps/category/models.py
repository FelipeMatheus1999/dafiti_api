from django.db import models
from django.utils.translation import gettext_lazy as _
from services.base_model import BaseModel


class CategoryModel(BaseModel):
    name = models.CharField(max_length=255, verbose_name=_("Category Name"))

    def __str__(self):
        return self.name

    class Meta:
        db_table = "category"
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")
