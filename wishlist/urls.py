
from django.contrib import admin
from django.urls import path,include
from .import views

urlpatterns = [
    path('add_to_wishlist/<int:variant_id>/',views.add_to_wishlist,name='add_to_wishlist'),
    path('list_wishlist/',views.list_wishlist,name='list_wishlist'),
    path('remove_wishlist_item/<int:variant_id>/',views.remove_wishlist_item,name='remove_wishlist_item'),

]
