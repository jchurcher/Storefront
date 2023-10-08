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
    path("cart/delete_from_cart/", views.delete_from_cart, name="delete_from_cart"),
    path("cart/change_item_quantity/", views.change_item_quantity, name="change_item_quantity"),
    path("create_order_from_cart/", views.create_order_from_cart, name="create_order_from_cart"),
]