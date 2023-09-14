from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from store.models import ProductVariant,Product,Coupon
from cart.models import Cart,Cart_Item,UserAddress
from django.contrib import messages
from django.db import transaction
from django.http import JsonResponse
from accounts.models import Account,Address
from django.db.models import Sum
from  django.urls import reverse
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from paypal.standard.forms import PayPalPaymentsForm
from django.http import HttpResponseRedirect
from .models import Product  # Import your models
from offer.models import Offer
from django.shortcuts import render
import paypalrestsdk  
from django.conf import settings
from django.shortcuts import render, redirect
from django.urls import reverse
from offer.models import Offer
import razorpay



def cart(request):
    user = request.user
    cart = Cart.objects.filter(user=user).first()
    offer =Offer.objects.all()
    productVariant =ProductVariant.objects.all()
    cart_item =Cart_Item.objects.all()

    if cart:
        cart_items = cart.cart_items.all()
    else:
        cart_items = []

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        cancel_coupon = request.POST.get('cancel_coupon')  # Check if Remove Coupon button was clicked

        if coupon_code and not cancel_coupon:  # Only apply coupon if not canceling
            coupon_obj = Coupon.objects.filter(Coupon_code__icontains=coupon_code).first()

            if not coupon_obj:
                messages.warning(request, 'Invalid coupon')
            
            else:
                if cart.get_total_price() < coupon_obj.minimum_amount:
                    messages.warning(request, f'Amount should be above {coupon_obj.minimum_amount}')
                elif coupon_obj.is_expired:
                    messages.warning(request, 'Coupon expired')
                elif cart.coupon and cart.coupon.is_expired:
                    messages.warning(request, 'the Coupon is Expired.')
                else:
                    cart.coupon = coupon_obj
                    cart.save()
                    messages.success(request, 'Coupon applied')

        elif cancel_coupon:
            cart.coupon = None  # Remove the coupon
            cart.save()
            messages.success(request, 'Coupon removed successfully')
    for cart_item in cart_items:
        # Access the 'quantity' attribute of the cart item
        quantity = cart_item.quantity
        
    total_price = cart.get_total_price()
    offer = sum(item.variant.get_offer_price() for item in cart_items)
    discount = total_price - (offer * quantity)

    if cart.coupon:
        total =  total_price - discount - cart.coupon.discount_price
    else:
        total = total_price - discount

    
    context = {
        'cart_items': cart_items,
        'cart': cart ,
        'offer': offer,
        'variant':productVariant,
        'total_price' : total,
        'discount': discount,
        'cart_item':cart_item,
        'quantity':quantity,
        'total':total
    }

    return render(request, 'userside/cart.html',context)


@login_required(login_url='user_login')
def add_to_cart(request, variant_id):
    user = request.user
    variant = get_object_or_404(ProductVariant, pk=variant_id)
    cart, _ = Cart.objects.get_or_create(user=user)
    

    if not variant.is_available or variant.stock_quantity <= 0:
            messages.warning(request, 'Out of stock')
            return redirect('shop')
    
    product = variant.product

    
    # If no variant is specified or variant is available, create or update the cart item
    cart_item, created= Cart_Item.objects.get_or_create(cart=cart, product=product, variant=variant)
    


    if not created:
        if variant is not None and cart_item.quantity >= variant.stock_quantity:
            messages.warning(request, 'Out of stock')
            return redirect('shop')
        else:
            cart_item.quantity += 1
            cart_item.save()

    messages.success(request, 'Added successfully')
    return redirect('shop')

   


# delete cart item
@login_required(login_url='user_login')
def delete_cart_item(request, cartitem_id):
    cart_item = get_object_or_404(Cart_Item, id=cartitem_id)
    
    if cart_item.cart.user != request.user:
        messages.error(request, 'You do not have permission to delete this item.')
        return redirect('cart')

    cart_item.delete()
    messages.success(request, 'Item removed from the cart.')
    return redirect('cart')


# increment cart item

@login_required(login_url='user_login')
def increment_cart_item(request, cartitem_id):
    cart_item = get_object_or_404(Cart_Item, id=cartitem_id)
    
    # Make sure the cart item belongs to the currently logged in user
    if cart_item.cart.user != request.user:
        messages.error(request, 'You do not have permission to update this item.')
        return redirect('cart')
    
    if cart_item.variant is not None and cart_item.quantity >= cart_item.variant.stock_quantity:
        messages.warning(request, 'Maximum quantity reached.')
    else:
        cart_item.quantity += 1
        cart_item.save()
        messages.success(request, 'Quantity updated successfully.')
    
    return redirect('cart')

# decrement cart item
def decrement_cart_item(request, cartitem_id):
    cart_item = get_object_or_404(Cart_Item, id=cartitem_id)
    
    
    if cart_item.cart.user != request.user:
        messages.error(request, 'You do not have permission to update this item.')
        return redirect('cart')
    
    if cart_item.quantity > 1:
        cart_item.quantity -= 1
        cart_item.save()
        messages.success(request, 'Quantity updated successfully.')
    else:
        messages.warning(request, 'Minimum quantity reached.')
    
    return redirect('cart')



@login_required(login_url='user_login')
def checkout(request):

    user = request.user
    cart, _ = Cart.objects.get_or_create(user=user)
    cart_products = cart.cart_items.all()  # Assuming the related name for items in Cart is 'cart_items'
    addresses = Address.objects.filter(user = user)
    offer =Offer.objects.all()
    productVariant =ProductVariant.objects.all()
    cart_item =Cart_Item.objects.all()
    product=Product.objects.all()
    
    
    if cart:
        cart_items = cart.cart_items.all()
    else:
        cart_items = []

    if request.method == 'POST':
        coupon_code = request.POST.get('coupon')
        cancel_coupon = request.POST.get('cancel_coupon')  # Check if Remove Coupon button was clicked

        if coupon_code and not cancel_coupon:  # Only apply coupon if not canceling
            coupon_obj = Coupon.objects.filter(Coupon_code__icontains=coupon_code).first()

            if not coupon_obj:
                messages.warning(request, 'Invalid coupon')
            
            else:
                if cart.get_total_price() < coupon_obj.minimum_amount:
                    messages.warning(request, f'Amount should be above {coupon_obj.minimum_amount}')
                elif coupon_obj.is_expired:
                    messages.warning(request, 'Coupon expired')
                elif cart.coupon and cart.coupon.is_expired:
                    messages.warning(request, 'the Coupon is Expired.')
                else:
                    cart.coupon = coupon_obj
                    cart.save()
                    messages.success(request, 'Coupon applied')

        elif cancel_coupon:
            cart.coupon = None  # Remove the coupon
            cart.save()
            messages.success(request, 'Coupon removed successfully')
    for cart_item in cart_items:
        # Access the 'quantity' attribute of the cart item
        quantity = cart_item.quantity
        single_product_price =  cart_item.get_total_price()
        total_price = cart.get_total_price()
        offer = sum(item.variant.get_offer_price() for item in cart_items)
        discount = total_price - (offer * cart_item.quantity)

        checkout_subtotal = (single_product_price * quantity )- offer

        if cart.coupon:
            total =  total_price - discount - cart.coupon.discount_price
        else:
            total = total_price - discount

        
        subtotal = total_price - discount

    total_quantity = cart_products.aggregate(Sum('quantity'))['quantity__sum'] or 0

    client = razorpay.Client(auth= ( settings.KEY, settings.KEY_SECRET ))
    payment = client.order.create({'amount' :int(total) * 100 , 'currency' :'INR', 'payment_capture' : 1 })

    context = {
        'total_quantity': total_quantity,
        'add': addresses, 
        'cart': cart,
        'cart_products': cart_products,
        'cart_item': cart_item,
        'cart': cart ,
        'offer': offer,
        'variant':productVariant,
        'total':total,
        'quantity':quantity,
        'subtotal':subtotal,
        'product':product,
        ' checkout_subtotal': checkout_subtotal,
        'payment':payment,


    }

    return render(request, 'userside/checkout.html', context)



def cancel_coupon(request):
    carts = Cart.objects.all()

    for cart in carts:
        if cart.coupon:
            cart.coupon = None
            cart.save()

    messages.success(request, 'All applied coupons removed')
    return redirect('cart') 


# ============================================payment=============================================
