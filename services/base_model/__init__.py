from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    date_joined = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Joined"))
    date_modified = models.DateTimeField(auto_now_add=True, verbose_name=_("Date Modified"))

    is_active = models.BooleanField(default=True)

    class Meta:
        abstract = True
