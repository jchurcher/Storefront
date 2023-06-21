from django.db import models

# Model required
#- Product
#   > title
#   > desc
#   > price
#   > inventory
#- Collection
#   > title
#   > featured_product
#- Cart
#   > created_at
#- CartItem
#   > quantity
#- Order
#   > placed_at
#- OrderItem
#   > quantity
#- Customer
#   > name
#   > email

class Product(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    price = models.DecimalField(decimal_places=2, max_digits=6)
    inventory = models.IntegerField()
    collection = models.ForeignKey(
        "Collection",
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="products",
    )

    def __str__(self):
        return str(self.title)

class Collection(models.Model):
    title = models.CharField(max_length=100)
    featured_product = models.ForeignKey(
        Product,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name="featured_in",
    )

    def __str__(self):
        return str(self.title)

class Cart(models.Model):
    created_at = models.DateTimeField()

class CartItem(models.Model):
    quantity = models.IntegerField()