from import_export import resources, fields
from import_export.widgets import DateTimeWidget, CharWidget, ManyToManyWidget, FloatWidget, IntegerWidget, BooleanWidget
from .models import ProductModel
from ..category.models import CategoryModel


class ProductResource(resources.ModelResource):
    id = fields.Field(attribute="id", column_name="Product ID", widget=CharWidget())
    title = fields.Field(
        attribute="title", column_name="Title", widget=CharWidget()
    )
    description = fields.Field(
        attribute="description", column_name="Description", widget=CharWidget()
    )
    image = fields.Field(
        attribute="image", column_name="Image", widget=CharWidget()
    )
    price = fields.Field(attribute="price", column_name="Price", widget=FloatWidget())
    stock = fields.Field(attribute="stock", column_name="Stock", widget=IntegerWidget())
    categories = fields.Field(
        attribute="categories", column_name="Categories", widget=ManyToManyWidget(separator=" | ", model=CategoryModel)
    )
    date_joined = fields.Field(
        attribute="date_joined", column_name="Date Joined", widget=DateTimeWidget()
    )
    date_modified = fields.Field(
        attribute="date_modified", column_name="Date Modified", widget=DateTimeWidget()
    )
    is_active = fields.Field(
        attribute="is_active", column_name="Is Active", widget=BooleanWidget()
    )

    class Meta:
        model = ProductModel
        fields = [
            "id",
            "title",
            "description",
            "image",
            "price",
            "stock",
            "categories",
            "date_joined",
            "date_modified",
            "is_active",
        ]
        export_order = fields
