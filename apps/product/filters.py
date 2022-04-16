from django_filters import rest_framework as filters

from .models import ProductModel


class ProductFilter(filters.FilterSet):
    id = filters.NumberFilter(field_name="id")
    is_active = filters.BooleanFilter(field_name="is_active")
    date_joined = filters.DateTimeFilter(field_name="date_joined", lookup_expr="gte")
    date_modified = filters.DateTimeFilter(field_name="date_modified", lookup_expr="gte")
    title = filters.CharFilter(field_name="title", lookup_expr="icontains")
    description = filters.CharFilter(field_name="description", lookup_expr="icontains")
    price = filters.NumberFilter(field_name="price", lookup_expr="exact")
    stock = filters.NumberFilter(field_name="stock", lookup_expr="exact")

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "is_active",
            "date_joined",
            "title",
            "description",
            "price",
            "stock",
        ]
