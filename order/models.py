from django.db import models
from accounts.models import Account,Address
from store.models import Product,ProductVariant
from decimal import Decimal
  


class Order(models.Model):
    STATUS_CHOICES = (
        ('PENDING', 'Pending'),
        ('PROCESSING', 'Processing'),  
        ('SHIPPED', 'Shipped'),
        ('DELIVERED', 'Delivered'),
        ('CANCELLED', 'Cancelled'),
        ('CONFIRMED','confirmed'),
    ) 
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='orders')
    address = models.ForeignKey(Address, on_delete=models.CASCADE, related_name='orders')
    total_price = models.DecimalField(max_digits=10, decimal_places=2,default=0)
    status = models.CharField(max_length=50,choices=STATUS_CHOICES,default='PENDING')
    payment_method = models.CharField(max_length=50)
    payment_id = models.CharField(max_length=100, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tracking_no = models.CharField(max_length=150,null=False)
    # tracking_number = models.CharField(max_length=150,null=False, default=0)
     
    def get_orderItem_count(self):
        count = sum(item.quantity for item in self.orderitems.all())
        return count  

    
    def calculate_total_price(self):
        total_price = sum(item.variant.price * item.quantity for item in self.orderitems.all())
        return total_price
    
    def calculate_cart_total(self):
        cart_total = Decimal(0)
        for order_item in self.orderitems.all():
            cart_total += order_item.calculate_item_total()
        return cart_total
   

    
class OrderItem(models.Model):
    # order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    # product = models.ForeignKey(Product, on_delete=models.CASCADE)
    # # variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    # quantity = models.PositiveIntegerField(default=1)
    # price = models.DecimalField(max_digits=6, decimal_places=2)

   

    def calculate_item_total(self):
        return self.product.price * self.quantity
    

class Order_product(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='orderitems')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=6, decimal_places=2)

   

    def calculate_item_total(self):
        return self.product.price * self.quantity

   