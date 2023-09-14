from . import views
from django.urls import path
from admindashboard.views import *
from django.contrib.auth.views import LogoutView


urlpatterns = [
    path('dashboard/',views.dashboard,name='dashboard'),
    path('adminproduct/', views.adminproduct, name='adminproduct'),
    path('adminuser/', views.adminuser, name='adminuser'),
    # --------------------------------------------------------------------------
    path('admincategory/', views.admincategory, name='admincategory'),
    path('delete_category/<int:category_id>',delete_category, name='delete_category'),
    path('edit_category/<int:category_id>/', views.edit_category, name='edit_category'),

    path('add_category/', views.add_category, name='add_category'),
    path('block/<int:user_id>',views.blockandunblock,name='block'),
    path('edit/<int:product_id>/', views.edit_products, name='edit_product'),
    path('add_product/', views.add_products, name='add_product'),
    path('delete_product/<int:product_id>', views.delete_product, name='delete_product'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
# ==================================order======================================
    path('order_management',order_management, name='order_management'),
    path('cancel_order/<int:order_id>',views.cancel_order, name='cancel_order'),
    path('update_order_status/<int:order_id>',update_order_status, name='update_order_status'),
    
# ======================================sales report=====================================
    path('salesreport/', views.salesreport, name='salesreport'),
    path('download_sales_report_csv', download_sales_report_csv, name='download_sales_report_csv'),
    path('download_sales_report', download_sales_report, name='download_sales_report'),



    path('coupon/', views.coupon, name='coupon'),
    path('edit_coupon/<int:coupon_id>/', views.edit_coupon, name='edit_coupon'),
    path('add_coupon/', views.add_coupon, name='add_coupon'),
    path('delete_coupon/<int:coupon_id>/', views.delete_coupon, name='delete_coupon'),

]

