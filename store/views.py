
from django.shortcuts import render,HttpResponse,redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib import messages
from django.core.exceptions import ValidationError
import random
from django.conf import settings
from django.core.mail import send_mail
from cart.models import Cart
from .models import Product,Coupon
from django.http import Http404
from category.models import category
from django.shortcuts import get_object_or_404
from accounts.models import Account 
from django.contrib.sessions.models import Session
from django.contrib.auth import update_session_auth_hash
from accounts.models import Address
from accounts.models import Account,Address
from django.contrib import messages
from .models import Product,ProductVariant,Image
from django.http import JsonResponse
from datetime import date
from django.utils import timezone



def home(request):
    products = Product.objects.filter(is_available=True)
    context = {
        'products': products,
    }
    return render(request, 'userside/home.html', context)


def register(request):
    return render(request, 'userside/register.html')

def shop(request,category_slug=None):
    categories = None
    products = None
    if category_slug != None:
        categories = category.objects.get(slug=category_slug)
        products = Product.objects.filter(category=categories,is_available=True)
    else:

        products =  Product.objects.all().filter(is_available=True)

    products = ProductVariant.objects.all()    

    context= {
        'products':products,
    }

    return render(request,'userside/shop.html',context)





def single_page(request,singel_id):
    pr=Product.objects.get(id=singel_id)
    context={
        'product':pr,
    }

    return render(request,'userside/productdetails.html',context)




def about(request):
    return render(request,'userside/about.html')


def wishlist(request):
    return render(request,'userside/wishlist.html')


def adminproduct(request):
    return render(request,'userside/productadmin.html')

def productdeatils(request,product_id):
    variant = ProductVariant.objects.get(id=product_id)
    variants = ProductVariant.objects.filter(product=variant.product)

    context = {
       'variants':variants,
        'product':variant,
    }

    return render(request,'userside/productdetails.html',context)


# ======================================offer==================================================




def edit_product_variant(request,variant_id):
    
    variant = get_object_or_404(ProductVariant,id = variant_id)
    
    if request.method == 'POST':
        material = request.POST['material']
        price = request.POST['price']
        stock = request.POST['stock']
        image = request.FILES.get('image')
        
        variant.material = material
        variant.price = price
        variant.stock_quantity = stock
        variant.save()
        if image is None:
            pass
        else:
            Image.objects.create(product_variant = variant,image = image)
        product_id = variant.product.id
        messages.success(request,'updated')
        return redirect('admin_variant_list',product_id)
        
    
    return render(request,'c_admin/editproduct_variant.html',{'variant':variant})    
        

# delete variant image
def delete_variant_image(request,image_id):
    image = get_object_or_404(Image,id = image_id)
    variant_id = image.product_variant.id
    image.delete()
    return redirect('edit_product_variant',variant_id)
      
# soft delete product
def soft_delete_product(request,variant_id):
    variant = get_object_or_404(ProductVariant,id = variant_id)
    if variant.is_available:
        variant.is_available = False
        variant.save()
        product_id = variant.product.id
        return redirect('admin_variant_list',product_id)
    else:
        variant.is_available = True
        variant.save()
        product_id = variant.product.id
        return redirect('admin_variant_list',product_id)
    
# search variant 
def admin_variant_search(request,product_id):
    
    key = request.GET['key']
    variants = ProductVariant.objects.filter(product__id = product_id)
    product = Product.objects.get(id = product_id)
        
    if key is not None:
        variants = variants.filter(material__icontains = key)
            
    context = {
        'variants': variants,
        'key': key,
        'product':product
    }  
    
    return render(request,'c_admin/variantlist.html',context)  


def returnpolicy(request):
    return render(request, 'userside/returnpolicy.html')



def refer(request):
    user = request.user
    referral_code = user.refferal_code1 if hasattr(user, 'refferal_code1') else None
    signup_link = user.refferal_link if hasattr(user, 'refferal_link') else None

    context = {'ref_link': signup_link, 'ref_code': referral_code}

    return render(request, 'userside/refer.html', context)

def couponlist(request):
   
    current_datetime = timezone.now()
    
    # Filter coupons that are not expired
    not_expired_coupons = Coupon.objects.filter(end_date__gte=current_datetime)

    return render(request,'userside/couponlist.html',{'coupon_shows':not_expired_coupons})