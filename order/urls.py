
from django.urls import path
from .import views


urlpatterns = [
  path('order/', views.order, name='order'),
  
  path('summary/<int:id>', views.summary, name='summary'),
  path('place_order/', views.place_order, name='place_order'),
  path('place_order_razorpay/', views.place_order_razorpay, name='place_order_razorpay'),
  path('order_detail/', views.order_detail, name='order_detail'),
 path('orderview/', views.orderview, name='orderview'),
 path('remove_order/<int:order_id>/', views.remove_order, name='remove_order'),
 path('shipped/<int:order_id>/', views.shipped, name='shipped'),
  path('delivered/<int:order_id>/', views.delivered, name='delivered'),
  path('completed/<int:order_id>/', views.completed, name='completed'),
  path('ordertracking/<int:order_id>', views.ordertracking, name='ordertracking'),
  path('invoice/<int:order_id>', views.invoice, name='invoice'),
  
]
