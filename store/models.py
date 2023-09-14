from django.db import models
from django.contrib.auth.models import User
from offer.models import Offer
from decimal import Decimal

from category.models import category


 
    
class Product(models.Model):
    product_name = models.CharField(max_length=200,unique = True)
    description = models.TextField(max_length=255,blank=True)
    price = models.IntegerField(null=True)
    product_slug = models.CharField(max_length=200,null=True)
    cat_image = models.ImageField(upload_to='photos/products',)
    offer = models.ForeignKey(Offer, on_delete=models.CASCADE, null=True, blank=True)
    stock = models.IntegerField()
    is_available = models.BooleanField(default=True)
    category =models.ForeignKey(category,on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)

    def get_color_variants(self):
        return self.color_variants.all()
    
    
      
      
   
    def __str__(self):
        return self.product_name

    
class ProductVariant(models.Model):
    material = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='variants')
    price = models.DecimalField(max_digits=25, decimal_places=2)
    stock_quantity = models.PositiveIntegerField(default=0)
    is_available = models.BooleanField(default=True)
     
    
    def __str__(self):
        return self.material+' '+self.product.product_name
    
    def change_price(self):
        return self.price+150
    
    def get_variant_image(self):
        
        product_image = self.images.first()
        
        if product_image:
                
            return product_image.image.url   
            
        else:
                
            return '/static/user/media/brand/1.jpg'    
        
    def get_offer_price(self):
       
        if self.product.offer:

            discount_percentage = Decimal(self.product.offer.discount_percentage)
             # Convert the discount percentage to Decimal
            return Decimal(self.price - (self.price * discount_percentage / Decimal(100))) 
        else:
            return self.price 

    def get_total_offer_price(self, cart_items):
        total_offer_price = sum(item.get_offer_price() for item in cart_items)
        return total_offer_price
    
    
class Image(models.Model):
 
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE,related_name='images')
    image = models.ImageField(upload_to='product/images/')


class Coupon(models.Model):
    Coupon_code = models.CharField(max_length=20)
    is_expired = models.BooleanField(default=False)
    end_date = models.DateField(null=True)
    
    discount_price = models.IntegerField(default=100)
    minimum_amount = models.IntegerField(default=500)

        
