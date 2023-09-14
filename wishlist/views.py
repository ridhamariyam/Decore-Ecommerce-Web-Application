from django.shortcuts import render,redirect
from store.models import ProductVariant
from .models import Wishlist
from django.contrib.auth.decorators import login_required

# Create your views here.

# add to wishlist
@login_required(login_url='user_login')
def add_to_wishlist(request,variant_id):
    
    user = request.user
    variant = ProductVariant.objects.get(id = variant_id)
    product_id = variant.product.id
    Wishlist.objects.get_or_create(user = user,product_variant = variant)
    return redirect('product_details',product_id)


# list wishlist
@login_required(login_url='user_login')
def list_wishlist(request):
    user = request.user
    wishlists = user.wishlists.all()
    return render(request,'userside/wishlist.html',{'wishlists':wishlists})


# remove from wishlist
def remove_wishlist_item(request,variant_id):
    user = request.user
    variant = ProductVariant.objects.get(id = variant_id)
    Wishlist.objects.filter(user = user,product_variant=variant).delete()
    return redirect('list_wishlist')
    


    