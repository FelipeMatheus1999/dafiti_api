from django.contrib import admin
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from .models import CategoryModel


@admin.register(CategoryModel)
class CategoryAdmin(admin.ModelAdmin):
    fieldsets = [
        [
            _("Identification"),
            {
                "fields": [
                    "name",
                ]
            },
        ],
        [
            _("Administration"),
            {"fields": ["date_joined", "date_modified", "is_active"]},
        ],
    ]
    readonly_fields = ["date_joined", "date_modified"]
    list_display = ["__str__", "date_joined", "date_modified"]
    list_filter = ["is_active", "date_joined", "date_modified"]
    search_fields = [
        "name",
    ]
    ordering = ["id"]
    list_per_page = 15

    def save_model(self, request, obj, form, change):
        obj.date_modified = timezone.now()
        obj.save()
