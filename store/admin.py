from django.contrib import admin

# Register your models here.

from .models import Product, Collection, Cart, CartItem, Order, OrderItem

class ProductInline(admin.TabularInline):
    model = Product
    extra = 3

class CollectionAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            "fields": (
                ["title", "featured_product"]
            ),
        }),
    )
    inlines = [ProductInline]

class CartItemInline(admin.TabularInline):
    model = CartItem

class CartAdmin(admin.ModelAdmin):
    readonly_fields = ["created_at"]
    inlines = [CartItemInline]

class OrderItemInline(admin.TabularInline):
    model = OrderItem

class OrderAdmin(admin.ModelAdmin):
    readonly_fields = ["placed_at"]
    inlines = [OrderItemInline]
    


admin.site.register(Product)
admin.site.register(Collection, CollectionAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(Order, OrderAdmin)