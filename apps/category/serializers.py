from rest_framework import serializers
from django.utils.translation import gettext_lazy as _

from apps.category.models import CategoryModel


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = CategoryModel
        fields = ("id", "name")

    def create(self, validated_data):
        name = validated_data.pop("name")
        category = CategoryModel.objects.get_or_create(name=name)[0]

        return category

    def update(self, instance, validated_data):
        name = validated_data["name"] if "name" in validated_data else None

        if name is not None:
            try:
                CategoryModel.objects.get(name=name)
                raise serializers.ValidationError({"detail": _("Category with this Category Name already exists.")})
            except CategoryModel.DoesNotExist:
                pass

        return super().update(instance, validated_data)
