from django.contrib import admin
from django.urls import path, include

admin.site.site_header = "Dafiti"
admin.site.site_title = "Dafiti"
admin.site.index_title = "Dafiti"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("grappelli/", include("grappelli.urls")),
    path("api/v1/", include("apps.user.urls")),
    path("api/v1/", include("apps.product.urls")),
    path("api/v1/", include("apps.category.urls")),
]
