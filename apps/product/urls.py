from django.urls import path
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet

router = DefaultRouter()
router.register("product", ProductViewSet)

urlpatterns = [
    path("product/export/csv/", ProductViewSet.as_view({"get": "export_csv_file"})),
    path("product/import/csv/", ProductViewSet.as_view({"post": "import_csv_file"})),
] + router.urls
