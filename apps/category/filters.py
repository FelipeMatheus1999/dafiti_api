from django_filters import rest_framework as filters

from .models import CategoryModel


class CategoryFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id")
    is_active = filters.BooleanFilter(field_name="is_active")
    date_joined = filters.DateTimeFilter(field_name="date_joined", lookup_expr="gte")
    date_modified = filters.DateTimeFilter(
        field_name="date_modified", lookup_expr="gte"
    )
    name = filters.CharFilter(field_name="title", lookup_expr="icontains")

    class Meta:
        model = CategoryModel
        fields = [
            "id",
            "is_active",
            "date_joined",
            "name",
        ]
