from django.shortcuts import render
from django.views import generic

from store.models import Product, Collection

# Create your views here.

class ProductIndexView(generic.ListView):
    model = Product
    template_name = "store/index.html"

    def get_queryset(self):
        return Product.objects.filter(title__contains='e')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = "Products"
        return context
    
class ProductDetailView(generic.DetailView):
    model = Product
    template_name = "store/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_dict"] = {"title": context["object"].title,
                                  "description": context["object"].description,
                                  "price": context["object"].price,
                                  "inventory": context["object"].inventory,
                                  "collection": context["object"].collection,}
        return context
    

    

class CollectionIndexView(generic.ListView):
    model = Collection
    template_name = "store/index.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = "Collections"
        return context