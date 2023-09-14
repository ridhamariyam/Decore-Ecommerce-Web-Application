from django.contrib import admin
from .models import Product,ProductVariant,Image,Coupon

class productAdmin(admin.ModelAdmin):
    list_display = ('product_name','price','stock','category','created_date','is_available')
    prepopulated_fields = {'slug':('product_name')}





admin.site.register(Product)
admin.site.register(ProductVariant)
admin.site.register(Image)
admin.site.register(Coupon)

