
from django.contrib import admin
from django.urls import path,include
from .import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from store.views import *

urlpatterns = [

    path('',views.home,name='home'), 
    path('about/',views.about,name='about'),
    path('shop/',views.shop,name='shop'),
    path('wishlist/',views.wishlist,name='wishlist'),
    path('refer/',views.refer,name='refer'),
    path('returnpolicy/',views.returnpolicy,name='returnpolicy'),
    path('couponlist/',views.couponlist,name='couponlist'),
    path('single_page/<int:singel_id>/',views.single_page,name='single_page'),
    path('product_details/<int:product_id>', views.productdeatils, name='product_details'),
    path('soft_delete_product/<int:variant_id>/',views.soft_delete_product,name='soft_delete_product'),

#    ==============================================VARIANT==============================

   
    path('edit_product_variant/<int:variant_id>/',views.edit_product_variant,name='edit_product_variant'),
    path('delete_variant_image/<int:image_id>/',views.delete_variant_image,name='delete_variant_image'),
    path('admin_variant_search/<int:product_id>/',views.admin_variant_search,name='admin_variant_search'),
   
   
]
