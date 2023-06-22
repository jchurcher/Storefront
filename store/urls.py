from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path("products/", views.ProductIndexView.as_view(), name="index_products"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="detail_products"),
    path("collections/", views.CollectionIndexView.as_view(), name="index_collections"),
]