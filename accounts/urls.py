
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from store.views import *

urlpatterns = [
  

    

    # =====================================PROFILE================================

    path('login/',views.handlelogin,name='login'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('changepassword/', views.changepassword, name='changepassword'),
    path('profile/', views.profile, name='profile'),
    path('generate_link/', views.generate_referral_code_and_signup_link, name='generate_link'),
    path('register/',views.register,name='register'),
    path('otp/', views.otp, name='otp'),
    path('logout/', LogoutView.as_view(), 
    name='logout'),

# =================================ADDRESS================================================
    path('address/', views.address,name='address'),
    path('add_address/', views.add_address,name='add_address'),
    path('update_address/<int:address_id>/',views.update_address,name='update_address'),
    path('delete_address/<int:address_id>/', views.delete_address,name='delete_address'),


    path('order_invoice/<int:order_id>', views.download_invoice, name='order_invoice'),

# =====================wallet==================================

    path('wallet/', views.wallet, name='wallet'),
   

]
