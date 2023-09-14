
from django.urls import path,include
from .import views

urlpatterns = [
   
    path('cart/', views.cart, name='cart'),
    path('add_to_cart/<int:variant_id>/',views.add_to_cart,name='add_to_cart'),
    path('delete_cart_item/<int:cartitem_id>/',views.delete_cart_item,name='delete_cart_item'),
    path('increment_cart_item/<int:cartitem_id>/',views.increment_cart_item,name='increment_cart_item'),
    path('decrement_cart_item/<int:cartitem_id>/',views.decrement_cart_item,name='decrement_cart_item'),
    path('checkout/', views.checkout, name='checkout'),
    
    path('cancel_coupon/', views.cancel_coupon, name='cancel_coupon'), 
   
  



]
