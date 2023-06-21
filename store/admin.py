from django.contrib import admin

# Register your models here.

from .models import Product, Collection

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
    


admin.site.register(Product)
admin.site.register(Collection, CollectionAdmin)