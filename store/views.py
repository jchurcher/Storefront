from typing import Any, Dict
from django import http
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import generic

from store.models import Product, Collection, Cart, CartItem

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
    template_name = "store/product.html"

    # def get_context_data(self, **kwargs):
    #     context = super().get_context_data(**kwargs)
    #     obj_dict = model_to_dict(context["object"], exclude="id")
    #     # context["object_dict"] = obj_dict
    #     return context
    

    

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
    template_name = "store/collection.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured_product = context["object"].featured_product
        context["object_list"] = context["object"].products.exclude(pk=featured_product.id)
        context["detail_url"] = 'detail_products'
        return context
    

class CartIndexView(generic.ListView):
    model = CartItem
    template_name = "store/cart.html"
    context_object_name = "items_in_cart"

    cart = None

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        self.cart = Cart.objects.get(pk=request.session["cart"])
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        cart_items = self.cart.cart_items.all()
        for item in cart_items:
            item.getTotal()
        return cart_items
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        context["cart"] = self.cart
        self.cart.getTotal()

        return context
    


def add_to_cart(request, product_id, quantity=1):
    current_product = Product.objects.get(pk=product_id)

    if "cart" in request.session:
        current_cart = Cart.objects.get(pk = request.session["cart"])
    else:
        current_cart = Cart()
        request.session["cart"] = current_cart.id

    cart_items = current_cart.cart_items.filter(product=product_id)

    if len(cart_items) > 0:
        current_cart_item = cart_items[0]
        current_cart_item.quantity += quantity
    else:
        current_cart_item = CartItem(quantity=quantity,
                                     product=current_product,
                                     cart=current_cart)

    current_cart.save()
    current_cart_item.save()

    request.session["banner"] = str(quantity) + " " + current_product.title + " has been added to your cart"

    return redirect("detail_products", product_id)

def delete_from_cart(request, product_id):
    current_cart = Cart.objects.get(pk = request.session["cart"])

    cart_item = CartItem.objects.get(pk = product_id, cart=current_cart)
    
    cart_item.delete()

    request.session["banner"] = cart_item.product.title + " has been deleted from your cart"

    return redirect("index_cart_items")

def change_item_quantity(request, product_id):
    if request.method == "GET":
        new_quantity = request.GET["quantity"]

    current_cart = Cart.objects.get(pk = request.session["cart"])

    cart_item = CartItem.objects.get(pk = product_id, cart=current_cart)
    cart_item.quantity = new_quantity
    cart_item.save()

    request.session["banner"] = "Quantity of " + cart_item.product.title + " changed to " + new_quantity

    return redirect("index_cart_items")