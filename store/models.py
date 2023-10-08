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
    photo = models.ImageField(upload_to='products', default='default_image.jpg')
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
    created_at = models.DateTimeField(auto_now_add=True, blank=True)

    totalPrice = None

    def getTotal(self):
        self.totalPrice = sum([x.getTotal() for x in self.cart_items.all()])
        return self.totalPrice
    
    def cartItemsToJSON(self):
        newString = "{"
        for item in self.cart_items.all():
            newString += "{} : {{price: {}, quantity: {}}},".format(item.id, item.product.price, item.quantity)
        newString = newString[0:-1]
        newString += "}"

        return newString

class CartItem(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(
        Product,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="cart_items",
    )
    cart = models.ForeignKey(
        Cart,
        blank=False,
        null = False,
        on_delete=models.CASCADE,
        related_name="cart_items"
    )

    # totalPrice = None
    
    # def getTotal(self):
    #     self.totalPrice = self.quantity * self.product.price
    #     return self.totalPrice
    
    def getTotal(self):
        return self.quantity * self.product.price
    
class Order(models.Model):
    placed_at = models.DateField(auto_now_add=True, blank=True)

    totalPrice = None

    def getTotal(self):
        self.totalPrice = sum([x.getTotal() for x in self.cart_items.all()])
        return self.totalPrice
    
    def cart_to_order(self, cart):
        for item in cart.cart_items.all():
            quantity = item.quantity
            product = item.product
            self.order_items.create(quantity=quantity, product=product)

class OrderItem(models.Model):
    quantity = models.IntegerField()
    product = models.ForeignKey(
        Product,
        blank=False,
        null=False,
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    order = models.ForeignKey(
        Order,
        blank=False,
        null = False,
        on_delete=models.CASCADE,
        related_name="order_items"
    )

    def __str__(self):
        return self.product.title