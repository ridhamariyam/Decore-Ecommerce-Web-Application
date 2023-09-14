from . import views
from django.urls import path 

urlpatterns = [
    path('adminoffer/', views.adminoffer, name='adminoffer'),
    path('addoffer/',views.add_offer, name='add_offer'),
    path('remove_offer/<int:offer_id>/', views.remove_offer, name='remove_offer'),
    path('apply_offer/', views.apply_offer, name='apply_offer'),
]