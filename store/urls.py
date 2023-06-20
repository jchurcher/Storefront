from django.urls import path
from . import views

# URLConf
urlpatterns = [
    path("products/", views.IndexView.as_view(), name="index_products"),
]