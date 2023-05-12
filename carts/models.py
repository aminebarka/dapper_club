from django.db import models
from accounts.models import Account
from store.models import Product, ProductAttribute

# Create your models here.

    
 
class Cart(models.Model):
    cart_id = models.CharField(max_length=250, blank=True)
    date_added = models.DateField(auto_now_add=True, null=True)

    def __str__(self):
        return self.cart_id


class CartItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(ProductAttribute, on_delete=models.CASCADE, null=True)
    cart    = models.ForeignKey(Cart, on_delete=models.CASCADE, null=True)
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)


class WishlistItem(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    is_active = models.BooleanField(default=True)


class Coupon(models.Model):
    coupon_code = models.CharField(max_length=10)
    is_active = models.BooleanField(default=True)
    discount_price = models.IntegerField(default=199)
    minimum_amount = models.IntegerField(default=999)
    created_date = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    modify_date = models.DateTimeField(auto_now=True)
    expiry_date = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.coupon_code 