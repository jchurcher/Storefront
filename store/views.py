from typing import Any, Dict
from django import http
from django.db.models.query import QuerySet
from django.forms.models import model_to_dict
from django.http import HttpRequest, HttpResponse
from django.shortcuts import redirect, render
from django.views import generic

from store.models import Product, Collection, Cart, CartItem, Order, OrderItem

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
    context_object_name = "product"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        cart = Cart.objects.get_or_create(pk=self.request.session["cart"])[0]
        try:
            cartItem = cart.cart_items.get(product=context["product"])
        except:
            cartItem = None
        context["cartItem"] = cartItem

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
    template_name = "store/collection.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        featured_product = context["object"].featured_product
        if featured_product != None:
            context["object_list"] = context["object"].products.exclude(pk=featured_product.id)
        else:
            context["object_list"] = context["object"].products.all()
        
        context["detail_url"] = 'detail_products'
        return context
    

class CartIndexView(generic.ListView):
    model = CartItem
    template_name = "store/cart.html"
    context_object_name = "items_in_cart"

    cart = None

    def dispatch(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        # Get the cart object from db or create a new one
        if "cart" in request.session:
            self.cart = Cart.objects.get(pk=request.session["cart"])
        else:
            self.cart = Cart()
            self.cart.save()
            request.session["cart"] = self.cart.id
        
        return super().dispatch(request, *args, **kwargs)

    def get_queryset(self) -> QuerySet[Any]:
        cart_items = self.cart.cart_items.all()
        for item in cart_items:
            item.getTotal()
        return cart_items
    
    def get_context_data(self, **kwargs: Any) -> Dict[str, Any]:
        context = super().get_context_data(**kwargs)

        # Make cart and total price accessible from template
        context["cart"] = self.cart
        self.cart.getTotal()

        # Format data for javascript

        return context
    

#AJAX
    
# Adds an item to the cart by an id provided as a POST variable
def add_to_cart(request, quantity=1):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

    current_product = Product.objects.get(pk=product_id)

    if "cart" in request.session:
        current_cart = Cart.objects.get(pk = request.session["cart"])
    else:
        current_cart = Cart.objects.create()
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

    return HttpResponse("///Display this in banner (Added item to cart)///")

# Deletes and item from the cart by an id provided from a POST variable
def delete_from_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")

    current_cart = Cart.objects.get(pk = request.session["cart"])
    cart_item = CartItem.objects.get(product = product_id, cart=current_cart)
    
    cart_item.delete()

    request.session["banner"] = cart_item.product.title + " has been deleted from your cart"

    return HttpResponse("///Display this in banner (Deleted cart item)///")

# Changes the quantity of an item in the cart, item and quantity are provided as POST method variables
def change_item_quantity(request):
    if request.method == "POST":
        new_quantity = request.POST["quantity"]
        product_id = request.POST["product_id"]

    current_cart = Cart.objects.get(pk = request.session["cart"])

    cart_item = CartItem.objects.get(product = product_id, cart=current_cart)
    cart_item.quantity = new_quantity
    cart_item.save()

    request.session["banner"] = "Quantity of " + cart_item.product.title + " changed to " + new_quantity

    return HttpResponse("///Display this in banner (Changed item quantity)///")

def create_order_from_cart(request):
    if request.method != "POST":
        return None
    
    cart = request.POST["cart_id"]
    cart = Cart.objects.get(pk=cart)

    new_order = Order()
    new_order.save()
    new_order.cart_to_order(cart)

    cart.delete()
    del request.session["cart"]

    return redirect("index_cart_items")