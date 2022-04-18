from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import ProductModel
from .resources import ProductResource


@admin.register(ProductModel)
class ProductsAdmin(ImportExportModelAdmin):
    resource_class = ProductResource
    fieldsets = [
        [
            _("Identification"),
            {"fields": ["title", "description", "image", "categories"]},
        ],
        [
            _("Pricing"),
            {
                "fields": [
                    "price",
                ]
            },
        ],
        [
            _("Stock Control"),
            {
                "fields": [
                    "stock",
                ]
            },
        ],
        [
            _("Administration"),
            {"fields": ["date_joined", "date_modified", "is_active"]},
        ],
    ]
    readonly_fields = ["date_joined", "date_modified"]
    list_display = ["__str__", "price", "stock"]
    list_filter = ["is_active", "date_joined", "date_modified"]
    search_fields = [
        "title",
        "date_joined",
        "date_modified",
    ]
    ordering = ["id"]
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        obj.date_modified = timezone.now()
        obj.save()
