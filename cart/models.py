from django.db import models
from accounts.models import Account
from store.models import Product,ProductVariant,Coupon
from django.conf import settings
from decimal import Decimal


# Create your models here.

class Cart(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    coupon = models.ForeignKey(Coupon,on_delete=models.SET_NULL,null=True,blank = True)
    is_paid = models.BooleanField(default=False)

   


    def get_total_price(self):
        total_price = sum(item.get_total_price() for item in self.cart_items.all())


        return total_price 
    
    
class Cart_Item(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE,related_name='cart_items')
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, null=True, blank=True)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE,related_name='cart_items')
    quantity = models.PositiveIntegerField(default=1) 
    
    def get_total_price(self):
        if self.variant is not None:
            return self.variant.price * self.quantity
        else:
            return self.product.price * self.quantity        
    
    # def get_total_price(self):
    #     return self.quantity * self.total_price
    
class UserAddress(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE,related_name='addresses')
    address_name = models.CharField(max_length=50)
    name = models.CharField(max_length=50)
    street = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postcode = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=50)
    
 