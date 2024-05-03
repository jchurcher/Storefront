from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path("", views.HomePageView.as_view(), name="homepage"),

    #Products
    path("products/", views.ProductIndexView.as_view(), name="index_products"),
    path("products/<int:pk>/", views.ProductDetailView.as_view(), name="detail_products"),

    #Collections
    path("collections/", views.CollectionIndexView.as_view(), name="index_collections"),
    path("collections/<int:pk>/", views.CollectionDetailView.as_view(), name="detail_collections"),

    #Cart
    path("cart/", views.CartIndexView.as_view(), name="index_cart_items"),
    
    #Ajax
    path("add_to_cart/", views.add_to_cart, name="add_to_cart"),
    path("change_item_quantity/", views.change_item_quantity, name="change_item_quantity"),
    path("create_order_from_cart/", views.create_order_from_cart, name="create_order_from_cart"),
    path("delete_from_cart/", views.delete_from_cart, name="delete_from_cart"),
]