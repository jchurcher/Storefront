from django.http import HttpResponse
from django.shortcuts import render
from django.views import generic

from store.models import Product, Collection

# Create your views here.

class HomePageView(generic.TemplateView):
    template_name = "store/homepage.html"

class ProductIndexView(generic.ListView):
    model = Product
    template_name = "store/index.html"

    # def get_queryset(self):
    #     return Product.objects.filter(title__contains='e')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["model_name"] = "Products"
        context["detail_url"] = 'detail_products'
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
        context["detail_url"] = 'detail_collections'
        return context
    
class CollectionDetailView(generic.DetailView):
    model = Collection
    template_name = "store/detail.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["object_dict"] = {"title": context["object"].title,
                                  "featured_product": context["object"].featured_product.title,}
        return context