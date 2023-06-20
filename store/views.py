from django.shortcuts import render
from django.views import generic

from store.models import Product

# Create your views here.

class IndexView(generic.ListView):
    model = Product
    template_name = "store/index.html"