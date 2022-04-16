from rest_framework import serializers
from .models import ProductModel
from apps.category.models import CategoryModel
from ..category.serializers import CategorySerializer


class ProductSerializer(serializers.ModelSerializer):
    categories = CategorySerializer(many=True)

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "title",
            "description",
            "image",
            "price",
            "stock",
            "date_joined",
            "date_modified",
            "is_active",
            "categories"
        ]

    def create(self, validated_data):
        categories = validated_data.pop("categories") if "categories" in validated_data else []
        categories = [
            CategoryModel.objects.get_or_create(**category)[0].id
            for category in categories
        ]

        instance = ProductModel.objects.create(**validated_data)

        instance.categories.add(*categories)

        return instance

    def update(self, instance, validated_data):
        categories = validated_data.pop("categories") if "categories" in validated_data else None

        instance = super().update(instance, validated_data)

        if categories is not None:
            categories = [
                CategoryModel.objects.get_or_create(**category)[0]
                for category in categories
            ]

            instance.categories.set(categories)

        return instance
