from django.shortcuts import render
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Order,Order_product
from accounts.models import Account,Address,Wallet
from cart.models import Cart,Cart_Item
from django.db.models import Sum
from django.http import JsonResponse
import random
from datetime import datetime, timedelta
from django.contrib import messages
from offer.models import Offer
from cart.models import Cart,Cart_Item,UserAddress
from flask import Flask, render_template, make_response
from io import BytesIO
from django.http import JsonResponse




def order(request):
    
    orders = Order.objects.filter(user=request.user)
    return render(request,'userside/sum.html',{'orders': orders})



def orderview(request):
    orders = Order.objects.all()
    
    return render(request,'userside/ordersummary.html',{'orders': orders})



def order_detail(request):



    ord=Order_product.objects.filter(order__user=request.user,).order_by('-order__created_at')
    print(ord,'--------------------------')
    return render(request, 'userside/sum.html',{'order':ord})



def summary(request, id): 
    new_order = Order.objects.get(id = id)
    context = {'new_order': new_order}
    return render(request, 'userside/summary.html', context)



def place_order(request):
    if request.method == 'POST':
        user = request.user
        address_id = request.POST.get('selected_address')
        if not address_id:
        # User didn't select an address, display an error message
            user_addresses = Address.objects.filter(user=user)
            error_message = 'Please select an address to proceed.'
            return render(request, 'userside/checkout.html', {'user_addresses': user_addresses, 'error_message': error_message})
        
    
        selected_address = get_object_or_404(Address, id=address_id, user=user)
        payment_method = 'COD'
        
        user_cart = Cart.objects.filter(user=user, is_paid=False).last()
        if not user_cart:
           
            # Handle the case where the cart is empty or already paid
            return redirect('home')

        new_order = Order()
        new_order.user = user
        new_order.address = selected_address
        new_order.payment_method = payment_method
        new_order.total_price = user_cart.get_total_price()  
        track_no = 'RR' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = 'RR' + str(random.randint(1111111, 9999999))
        
        new_order.tracking_no = track_no
        new_order.save()

        return_deadline = datetime.now() + timedelta(days=14)

        # the return_deadline to the order
        new_order.return_deadline = return_deadline
        new_order.save() 

        
        cart_items = user_cart.cart_items.all()
        
        for cart_item in cart_items:
            order_item = Order_product() 
            print('orderitem.........................................',order_item)
            order_item.order = new_order
            order_item.product = cart_item.product
            order_item.variant = cart_item.variant
            order_item.price = cart_item.get_total_price()  
            order_item.quantity = cart_item.quantity
            
            print('orderitem.........................................',order_item)
            order_item.save()

            
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        user_cart.delete()

        new_order.status = 'confirmed'
        new_order.save()
        
        context = {'new_order': new_order}
        return render(request, 'userside/summary.html', context)
    print('-----------')
    # Retrieve user addresses
    user_addresses = Address.objects.filter(user=request.user)
    return render(request, 'userside/checkout.html', {'user_addresses': user_addresses})

# =============================================order status =================================

def remove_order(request, order_id):
    user = request.user 
    order = get_object_or_404(Order, id=order_id)

    # Increase the product stock for each order item (if needed)
    order_items = order.orderitems.all()
    for order_item in order_items:
        product = order_item.product
        product.stock += order_item.quantity
        product.save()

    # Delete the order
    order.status = 'Cancelled'
    order.save()

    user_wallet = Wallet.objects.get(userr=user)  
    user_wallet.balance += order.total_price  # Assuming total_amount is the order total
    user_wallet.save()

    messages.warning(request, 'Order has been cancelled and deleted successfully.')

    return redirect('order')

def shipped(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Update the order status to "Shipped" or whatever status you use
    order.status = 'Shipped'
    order.save()
    
    messages.warning(request, 'Order has been shipped successfully.')
    return redirect('order')

def delivered(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Update the order status to "Shipped" or whatever status you use
    order.status = 'delivered'
    order.save()
    
    messages.warning(request, 'Order has been shipped successfully.')
    return redirect('order')


def completed(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    
    # Update the order status to "Shipped" or whatever status you use
    order.status =  'completed'
    order.save()
    
    messages.warning(request, 'Order has been completed successfully.')
    return redirect('order')


# ==================================orderTracking============================

def ordertracking(request,order_id):
    order = Order.objects.get(id=order_id)
    estimated_delivery_date = order.created_at + timedelta(days=7)
    return render(request,'userside/ordertracking.html',{'order': order,'estimated_delivery_date':estimated_delivery_date})


# ===================================invoice=======================================

def invoice(request,order_id):
    if request.method == 'POST':
        user = request.user
        address_id = request.POST.get('selected_address')

    order = Order.objects.get(id=order_id)
    order_items = Order_product.objects.filter(order=order)
    print('ddddddddddddddddddddddddddddddddd',order_items)
   
    
    context={
        'order': order,
        'order_items':order_items

    }
   
           
    
    return render(request,'userside/invoice.html',context)


def place_order_razorpay(request):
    if request.method == 'POST':
        user = request.user
        address_id = request.POST.get('address')
    
        selected_address = get_object_or_404(Address, id=address_id, user=user)
        payment_method = 'Razorpay'
        
        user_cart = Cart.objects.filter(user=user, is_paid=False).last()
        if not user_cart:
           
            # Handle the case where the cart is empty or already paid
            return redirect('home')

        new_order = Order()
        new_order.user = user
        new_order.address = selected_address
        new_order.payment_method = payment_method
        new_order.total_price = user_cart.get_total_price()  
        track_no = 'RR' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=track_no).exists():
            track_no = 'RR' + str(random.randint(1111111, 9999999))
        
        new_order.tracking_no = track_no
        new_order.save()

        return_deadline = datetime.now() + timedelta(days=14)

        # the return_deadline to the order
        new_order.return_deadline = return_deadline
        new_order.save() 

        
        cart_items = user_cart.cart_items.all()
        
        for cart_item in cart_items:
            order_item = Order_product() 
            print('orderitem.........................................',order_item)
            order_item.order = new_order
            order_item.product = cart_item.product
            order_item.variant = cart_item.variant
            order_item.price = cart_item.get_total_price()  
            order_item.quantity = cart_item.quantity
            
            print('orderitem.........................................',order_item)
            order_item.save()

            
            cart_item.product.stock -= cart_item.quantity
            cart_item.product.save()
        
        user_cart.delete()

        new_order.status = 'confirmed'
        new_order.save()
        
        context = {'new_order': new_order}
        return JsonResponse({'status':"Your order has been placed successfully.", 'order' : new_order.id})
    print('-----------')
    # Retrieve user addresses
    user_addresses = Address.objects.filter(user=request.user)
    context = {'new_order': new_order}
    
    return render(request, 'userside/checkout.html', {'user_addresses': user_addresses})

