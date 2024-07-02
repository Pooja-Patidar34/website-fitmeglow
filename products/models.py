
# products/models.py
from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

class ProductType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SkinConcern(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class SkinType(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='products/images/')
    product_types = models.ManyToManyField(ProductType, blank=True)
    skin_concerns = models.ManyToManyField(SkinConcern, blank=True)
    skin_types = models.ManyToManyField(SkinType, blank=True)
    ingredients = models.TextField(blank=True, null=True)
    usage = models.TextField(blank=True, null=True)
    is_in_stock = models.BooleanField(default=True)

    @property
    def current_price(self):
        return self.sale_price if self.sale_price is not None else self.price

    def is_on_sale(self):
        return self.sale_price is not None

    def __str__(self):
        return self.name


class Wishlist(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product)

    def add_to_wishlist(self, product):
        if product.is_in_stock:
            self.products.add(product)
        else:
            raise ValueError("Cannot add out-of-stock products to wishlist.")

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    products = models.ManyToManyField(Product, through='CartItem')

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=10, decimal_places=2, null=True)

    def save(self, *args, **kwargs):
        if not self.product.is_in_stock:
            raise ValueError("Cannot add out-of-stock products to cart.")
        if not self.price:
            self.price = self.product.current_price  # Use the current price of the product
        super().save(*args, **kwargs)

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def save(self, *args, **kwargs):
        if not self.price:
            self.price = self.product.current_price
        super().save(*args, **kwargs)