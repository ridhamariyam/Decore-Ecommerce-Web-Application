
from django.db import models
from accounts.models import Account
from store.models import ProductVariant
# Create your views here.

class Wishlist(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='wishlists')
    product_variant = models.ForeignKey(ProductVariant, on_delete=models.CASCADE, related_name='wishlists')
    created_at = models.DateTimeField(auto_now_add=True)