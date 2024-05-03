import random
from django.test import TestCase
from django.urls import reverse

from store.models import Cart, CartItem, Collection, Product

# Create your tests here.
class ProductIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 20 products for testing
        numberOfProducts = 20

        for product_id in range(numberOfProducts):
            Product.objects.create(
                title = "product {}".format(product_id),
                price = random.uniform(0, 20),
                inventory = random.randrange(1, 20)
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/store/products/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index_products'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index_products'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')

class ProductDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a product for testing
        Product.objects.create(
            title = "test product",
            price = random.uniform(0, 20),
            inventory = random.randrange(1, 20)
        )

    def test_view_url_exists_at_desired_location(self):
        product = Product.objects.get(id=1)
        response = self.client.get(f'/store/products/{product.id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        product = Product.objects.get(id=1)
        response = self.client.get(reverse('detail_products', args=[product.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        product = Product.objects.get(id=1)
        response = self.client.get(reverse('detail_products', args=[product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product.html')

    # Add a product to the cart through ajax
    def test_add_product_to_cart_ajax(self):
        product = Product.objects.get(id=1)
        response = self.client.post(reverse('add_to_cart'), data={"product_id": product.id})
        self.assertEqual(response.status_code, 200)

    # Change quantity of a product in the cart through ajax
    def test_change_product_quantity_in_cart_ajax(self):
        product = Product.objects.get(id=1)
        response = self.client.post(reverse('add_to_cart'), data={"product_id": product.id})
        self.assertEqual(response.status_code, 200)

        item = CartItem.objects.all()[0]
        new_quantity = 10 if item.quantity != 10 else 8
        response = self.client.post(reverse('change_item_quantity'), data={"product_id": product.id, "quantity": new_quantity})
        self.assertEqual(response.status_code, 200)

class CollectionIndexViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 10 collections
        numberOfCollections = 10

        for collection_id in range(numberOfCollections):
            Collection.objects.create(
                title = "collection {}".format(collection_id)
            )

    def test_view_url_exists_at_desired_location(self):
        response = self.client.get('/store/collections/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        response = self.client.get(reverse('index_collections'))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        response = self.client.get(reverse('index_collections'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/index.html')

    def test_view_lists_all_collections(self):
        response = self.client.get(reverse('index_collections'))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context['object_list']), 10)

class CollectionDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create 2 collections
        numberOfCollections = 2

        for collection_id in range(numberOfCollections):
            Collection.objects.create(
                title = "collection {}".format(collection_id)
            )

        # Create 20 products for testing
        numberOfProducts = 20

        # 10 for each collection
        for product_id in range(numberOfProducts):
            Product.objects.create(
                title = "product {}".format(product_id),
                price = random.uniform(0, 20),
                inventory = random.randrange(1, 20),
                collection = Collection.objects.get(id = (product_id % numberOfCollections)+1)
            )

        collection_1 = Collection.objects.get(id=1)
        collection_1.featured_product = collection_1.products.get(id=1)

    def test_view_url_exists_at_desired_location(self):
        for collection in Collection.objects.all():
            response = self.client.get(f'/store/collections/{collection.id}/')
            self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        for collection in Collection.objects.all():
            response = self.client.get(reverse('detail_collections', args=[collection.id]))
            self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        for collection in Collection.objects.all():
            response = self.client.get(reverse('detail_collections', args=[collection.id]))
            self.assertEqual(response.status_code, 200)
            self.assertTemplateUsed(response, 'store/collection.html')

    # Only products from this collection should be displayed on this page
    def test_list_only_products_in_collection(self):
        for collection in Collection.objects.all():
            response = self.client.get(reverse('detail_collections', args=[collection.id]))
            collection_products = collection.products.all()
            self.assertEqual(list(collection_products), list(response.context['object_list']))

    # The featured product should be displayed
    def test_featured_product_is_displayed(self):
        collection = Collection.objects.get(id=1)
        response = self.client.get(reverse('detail_collections', args=[collection.id]))
        self.assertTrue(response.context["object"])
        self.assertEqual(collection.featured_product, response.context["object"].featured_product)

    # If there is no featured product for this collection display nothing
    def test_null_featured_product_is_not_displayed(self):
        collection = Collection.objects.get(id=2)
        response = self.client.get(reverse('detail_collections', args=[collection.id]))
        self.assertTrue(response.context["object"])
        self.assertFalse(response.context["object"].featured_product)
        self.assertFalse(collection.featured_product)

class CartDetailViewTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Create a product for testing
        Product.objects.create(
            title = "test product",
            price = random.uniform(0, 20),
            inventory = random.randrange(1, 20)
        )

    def test_view_url_exists_at_desired_location(self):
        product = Product.objects.get(id=1)
        response = self.client.get(f'/store/products/{product.id}/')
        self.assertEqual(response.status_code, 200)

    def test_view_url_accessible_by_name(self):
        product = Product.objects.get(id=1)
        response = self.client.get(reverse('detail_products', args=[product.id]))
        self.assertEqual(response.status_code, 200)

    def test_view_uses_correct_template(self):
        product = Product.objects.get(id=1)
        response = self.client.get(reverse('detail_products', args=[product.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'store/product.html')

    # Remove item from the cart through ajax
    def test_add_product_to_cart_ajax(self):
        product = Product.objects.get(id=1)
        response = self.client.post(reverse('add_to_cart'), data={"product_id": product.id})
        self.assertEqual(response.status_code, 200)

    # Change quantity of an item in the cart through ajax
    def test_change_product_quantity_in_cart_ajax(self):
        product = Product.objects.get(id=1)
        response = self.client.post(reverse('add_to_cart'), data={"product_id": product.id})
        self.assertEqual(response.status_code, 200)

        item = CartItem.objects.all()[0]
        new_quantity = 10 if item.quantity != 10 else 8
        response = self.client.post(reverse('change_item_quantity'), data={"product_id": product.id, "quantity": new_quantity})
        self.assertEqual(response.status_code, 200)