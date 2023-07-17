from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path("", views.HomePageView.as_view(), name="homepage"),
    path("products/", views.ProductIndexView.as_view(), name="index_products"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="detail_products"),
    path("collections/", views.CollectionIndexView.as_view(), name="index_collections"),
    path("collections/<int:pk>/", views.CollectionDetailView.as_view(), name="detail_collections"),
    path("cart/", views.CartIndexView.as_view(), name="index_cart_items"),
    path("add_to_cart/<int:product_id>/", views.add_to_cart, name="add_to_cart"),
]