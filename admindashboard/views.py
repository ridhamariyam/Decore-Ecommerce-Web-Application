from django.shortcuts import render
from category.models import category
from django.shortcuts import render,redirect
from accounts.models import Account
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from order.models import Order,Order_product,Order_product
from django.shortcuts import get_object_or_404, redirect
from offer.views import Offer
from store.models import Product,Coupon,ProductVariant,Image
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control
from django.contrib.auth import logout,get_user_model
from offer.models import Offer
from cart.models import Cart
from django.db.models import Sum,DateTimeField,Count
from django.db.models.functions import TruncMonth
import json
from datetime import datetime, timedelta
from django.utils import timezone
from django.db.models import Q
from django.template.loader import get_template
from xhtml2pdf import pisa
from io import BytesIO
from django.contrib.auth.decorators import login_required
from django.utils import timezone
import csv
from django.http import HttpResponse
from category.models import category

# Create your views here.
def dashboard(request):
    if not request.user.is_superuser:
        return redirect('userside/home')
    
    total_revenue = Order.objects.aggregate(total_revenue=Sum('total_price'))['total_revenue'] or 0
    total_orders = Order.objects.count()
    # Calculating total products
    total_products = Product.objects.count()
    # Calculating monthly income
    monthly_income = Order.objects.annotate(month=TruncMonth('created_at')).values('month').annotate(total_income=Sum('total_price')).order_by('month')
    # Calculate total users
    total_users = Account.objects.count()
     
    payment_mode_counts = Order.objects.values('payment_method').annotate(order_count=Count('id'))

    # Extract labels and data for the transaction chart.
    labels = [item['payment_method'] for item in payment_mode_counts]
    data = [item['order_count'] for item in payment_mode_counts]  


    # Query to get the count of orders for each order status
    order_status_counts = Order.objects.values('status').annotate(order_count=Count('status'))
    

    # Extract labels and data for the chart
    order_labels = [item['status'] for item in order_status_counts]
    order_data = [item['order_count'] for item in order_status_counts]


    # Calculate the last 6 months from the current date
    today = datetime.now()
    last_six_months = [today.strftime('%B')]  # Initialize the list with the current month
    for i in range(1, 6):
        previous_month = today - timedelta(days=30*i)
        last_six_months.append(previous_month.strftime('%B'))


    # Calculate total sales for each of the last six months
    total_sales_data = []
    for i in range(6):
        start_date = today - timedelta(days=30*(i+1))
        end_date = today - timedelta(days=30*i)
        total_sales = Order.objects.filter(created_at__gte=start_date, created_at__lt=end_date).count()
        total_sales_data.append(total_sales)


    # Calculate total visitors for each of the last six months
    total_visitors_data = []
    for i in range(6):
        start_date = today - timedelta(days=30*(i+1))
        end_date = today - timedelta(days=30*i)
        total_visitors = Account.objects.filter(date_joined__gte=start_date, date_joined__lt=end_date).count()
        total_visitors_data.append(total_visitors)      

 
    
    top_selling_products =Product.objects.values('product_name').annotate(sales_count=Count('order_product')).order_by('-sales_count')[:3]
   
    # Create two lists to store product names and sales counts
    product_names = []
    sales_counts = []
    

    # Extract data from 'top_selling_products' and populate the lists
    for product in top_selling_products:
    
        shortened_name = shorten_product_name(product['product_name'])
        product_names.append(shortened_name)
        sales_counts.append(product['sales_count'])

  



    context = {
       'total_revenue': total_revenue,
        'total_orders': total_orders,
        'total_products': total_products,
       
        'monthly_income': monthly_income,
        'total_users': total_users,
        
        'labels': labels,
        'data': data,
        
        'months': last_six_months,
        'total_sales_data': total_sales_data,
        'total_visitors_data': total_visitors_data, 

        'order_labels': order_labels,
        'order_data': order_data,

        

        'product_names': product_names,
        'sales_counts': sales_counts,


        }

    return render(request,'admindashboard/dashboard.html',context)


def shorten_product_name(name, max_length=9):
    name_str = str(name) 
    if len(name_str) <= max_length:
        return name_str
    return name_str[:max_length - 2] + '..'

# -----------------------------------product----------------------------------------------------------

def adminproduct(request):
    products = Product.objects.all()
    offer = Offer.objects.all()
    context= {
        'products':products,
        'offers' : offer
    }

    return render(request,'admindashboard/productadmin.html',context)


# def edit_products(request,product_id):
#     product = Product.objects.get(id=product_id)
#     categories = category.objects.all() 

#     if request.method == 'POST':
#         name = request.POST['product_name']
#         description = request.POST['description']
#         price = request.POST['price']
#         stock = request.POST['stock']
#         category_id = request.POST['category']

#         category_obj = category.objects.get(id=category_id)

#         product.product_name = name
#         product.description = description
#         product.price = price
#         product.stock = stock
#         product.category = category_obj

#         product.save()
#         messages.success(request, 'Product has been edited successfully.')
        
    
#         return redirect('adminproduct')
    
#     context = {
#         'categories': categories,
#         'product': product,
#     }
   
#     return render(request, 'admindashboard/edit_product.html', context)

def edit_products(request, product_id):
    product = get_object_or_404(Product, pk=product_id)

    if request.method == 'POST':
        product.product_name = request.POST['name']
        category_id = request.POST['category']
        description = request.POST['description']

        categoryy = category.objects.get(id=category_id)

        product.category = categoryy
        product.description = description

        product.save()

        variant_materials = request.POST.getlist('variant_material')
        variant_prices = request.POST.getlist('variant_price')
        variant_stocks = request.POST.getlist('variant_stock')

        # Delete existing variants not included in the updated data
        existing_variants = ProductVariant.objects.filter(product=product)
        existing_variant_ids = [variant.id for variant in existing_variants]
        for i in range(len(variant_materials)):
            if i < len(existing_variants):
                variant = existing_variants[i]
                variant.material = variant_materials[i]
                variant.price = variant_prices[i]
                variant.stock_quantity = variant_stocks[i]
                variant.save()
                existing_variant_ids.remove(variant.id)
            else:
                variant = ProductVariant.objects.create(
                    product=product,
                    material=variant_materials[i],
                    price=variant_prices[i],
                    stock_quantity=variant_stocks[i]
                )

            j = 0
            while f'images_{i}_{j}' in request.FILES:
                images = request.FILES.getlist(f'images_{i}_{j}')
                for image in images:
                    Image.objects.create(product_variant=variant, image=image)
                j += 1

        # Delete any existing variants not included in the update
        ProductVariant.objects.filter(id__in=existing_variant_ids).delete()

        messages.success(request, 'Product updated successfully')
        return redirect('adminproduct')
    else:
        categories = category.objects.all()
        product_variants = ProductVariant.objects.filter(product=product)
        images = Image.objects.filter(product_variant__in=product_variants)
        
        return render(request, 'admindashboard/edit_product.html', {
            'product': product,
            'categories': categories,
            'product_variants': product_variants,
            'images': images
        })
    
def add_products(request):
    if request.method == 'POST':
        product_name = request.POST['name']
       
        category_id = request.POST['category']
        description = request.POST['description']
        
        
        categoryy = category.objects.get(id=category_id)
        
        product = Product.objects.create(
            product_name=product_name,
          
            category=categoryy,
            description=description,
            stock = 0
          
        )
        
        variant_materials = request.POST.getlist('variant_material')
        variant_prices = request.POST.getlist('variant_price')
        variant_stocks = request.POST.getlist('variant_stock')
        
        for i in range(len(variant_materials)):
            variant = ProductVariant.objects.create(
                product=product,
                material=variant_materials[i],
                price=variant_prices[i],
                stock_quantity=variant_stocks[i]
            )

            j = 0
            while f'images_{i}_{j}' in request.FILES:
                images = request.FILES.getlist(f'images_{i}_{j}')
                for image in images:
                    Image.objects.create(product_variant=variant, image=image)
                j += 1
        messages.success(request,'added product')
        return redirect('adminproduct') 
    else:
        # Render the form to add a new product
       
        categories = category.objects.all()
        return render(request,'admindashboard/add_product.html', { 'categories': categories})
    



def delete_product(request,product_id):
    product_obj = Product.objects.get(id=product_id)
    product_name = str(product_obj)
    product_obj.delete()
    
    return redirect('adminproduct')





# ______________________________________________________PRODUCT____________________________________________________________________


# ----------------------------------------------usermanagement----------------------------------------------------

def adminuser(request):
    users = Account.objects.all().order_by('first_name')
    return render(request,'admindashboard/user_management.html', {'users': users})

def blockandunblock(request,user_id):
    user = Account.objects.get(id=user_id)
    if user.is_block:
        user.is_block = False
    else:
        user.is_block = True

    user.save()

    return redirect('adminuser')


# ______________________________________________usermanagement___________________________________________________


# --------------------------------------category-------------------------------------------

def admincategory(request):
    categories = category.objects.all()  
    if request.method == 'POST':
        searched = request.POST.get('searched', '')  # Use get() to avoid KeyError
        categories = category.objects.filter(name__istartswith=searched)

    return render(request, 'admindashboard/category_management.html', {'categories': categories})

def add_category(request):
    
    if request.method == 'POST':
        name = request.POST['category_name']
        description = request.POST['description']

        if category.objects.filter(category_name=name).exists():
            messages.error(request, 'Category name already exists.')
            return redirect('add_category')  # Redirect to the add_category view

        if name.strip() == '' or description.strip() == '':
            messages.error(request, 'Fields cannot be empty.')
            return redirect('add_category')  # Redirect to the add_category view
        
        category.objects.create(category_name=name, description=description)
        messages.success(request, 'New Category created successfully.')
        return redirect('admincategory')  # Redirect to the add_category view

    return render(request, 'admindashboard/categ_add_admin.html')

def delete_category(request,category_id):

    if not request.user.is_superuser:
        return redirect('home')
    category_obj = category.objects.get(id=category_id)
    category_name = str(category_obj)
    category_obj.delete()
    messages.warning(request,f'{category_name} category deleted.')
    return redirect('admincategory')

def edit_category(request, category_id):
    if not request.user.is_superuser:
        return redirect('index')
    
    category_obj = category.objects.get(id=category_id)

    if request.method == 'POST':
        name = request.POST['category_name']
        description = request.POST['description']
       
        if category.objects.filter(category_name=name).exclude(id=category_obj.id).exists():
            messages.warning(request, 'Category name already exists.')
            return redirect('edit_category', category_id=category_id)
        
        category_obj.category_name = name
        category_obj.description = description

        category_obj.save()
        messages.success(request, 'Category edited successfully')
        return redirect('admincategory') 
    
    context = {
        'category': category_obj,
    }
            
    return render(request, 'admindashboard/edit_category.html', context)
# ---------------------------------END CATEGORY--------------------------------------

                            #   ORDERLIST   #



@login_required(login_url='user_login')
def order_management(request):

    if not request.user.is_superuser:
        return redirect('home')
    
    orders = Order.objects.all().order_by('-created_at')

    if request.method == 'POST':
        searched = request.POST['searched']
        orders = Order.objects.filter(tracking_no__istartswith=searched)
        return render(request,'admindashboard/manage_order.html',{'orders': orders})
    
    return render(request,'admindashboard/manage_order.html',{'orders': orders} )

@login_required(login_url='user_login')

def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)

    # Increase the product stock for each order item (if needed)
    order_items = Order_product.objects.all()
    for order_item in order_items:
        product = order_item.product
        product.stock += order_item.quantity
        product.save()

    # Delete the order
    order.status = 'Cancelled'
    order.save()

    messages.warning(request, 'Order has been cancelled and deleted successfully.')

    return redirect(order_management)



@login_required(login_url='user_login')
def update_order_status(request, order_id):

    if not request.user.is_superuser:
        return redirect('index')
    
    order = get_object_or_404(Order, id=order_id)

    if request.method == 'POST':
        new_status = request.POST.get('new_status')
        order.status = new_status
        order.save()
        messages.warning(request,'Order status has been changed successfully.')

    return redirect('admindashboard/manage_order.html')





# ======================================sales report=======================================
@login_required(login_url='user_login')
def salesreport(request):

    if not request.user.is_superuser:
        return redirect('index')
    
    orders = Order.objects.all().order_by('-created_at')[:10] # Latest orders first

    # Get the start_date and end_date from the request's GET parameters
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Parse the date strings to datetime objects
    if start_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
    else:
        start_date = None

    if end_date_str:
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
    else:
        end_date = None

    # Ensure that the end date is not in the future
    today = timezone.now().date()
    if end_date and end_date.date() > today:
        messages.error(request, 'End date cannot be in the future.')
        return redirect('sales_report')
    
    # Ensure that the start date is not after the end date
    if start_date and end_date and start_date > end_date:
        messages.error(request, 'Start date cannot be after the end date.')
        return redirect('sales_report')


    # Filter orders based on date range if start_date and end_date are provided
    if start_date and end_date:
        orders =Order.objects.filter(created_at__range=(start_date, end_date)).order_by('-created_at')[:5]
    else:
        orders = Order.objects.all()
        
                

    

    context={
        'start_date': start_date_str,
        'end_date': end_date_str,
        'orders':orders
       
    }
    
    return render(request,'admindashboard/sales_report.html',context)


@login_required(login_url='user_login')
def download_sales_report_csv(request):

    if not request.user.is_superuser:
        return redirect('index')
    
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Perform date filtering on orders using start_date and end_date
    orders = Order.objects.all()
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        orders = orders.filter(created_at__range=[start_date, end_date])

    # Create CSV content
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="sales_report.csv"'
    writer = csv.writer(response)

    # Write CSV header
    writer.writerow(['Order ID', 'Payment Mode', 'Amount', 'Status', 'Ordered Date'])
    
    # Write CSV data rows
    for order in orders:
        writer.writerow([order.id, order.payment_method, order.total_price, order.status, order.created_at])

    return response




@login_required(login_url='user_login')
def download_sales_report(request):

    if not request.user.is_superuser:
        return redirect('index')
    
    start_date_str = request.GET.get('start_date')
    end_date_str = request.GET.get('end_date')

    # Perform date filtering on orders using start_date and end_date
    orders = Order.objects.all()
    if start_date_str and end_date_str:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d')
        orders = orders.filter(created_at__range=[start_date, end_date])

    # Render the sales report template with the filtered orders
    template = get_template('admindashboard/sales_report.html')
    context = {'orders': orders}
    html = template.render(context)

    # Create a PDF file from the HTML content
    response = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode('UTF-8')), response, link_callback=fetch_resources)
    if not pdf.err:
        response = HttpResponse(response.getvalue(), content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="sales_report.pdf"'
        return response

    return HttpResponse("Error generating PDF", status=500)

def fetch_resources(uri, rel):
    # Function to fetch external resources (e.g., CSS, images) for PDF generation
    # In this example, we assume that there are no external resources
    return uri


# ================================================COUPON============================================================================

@login_required(login_url='user_login')
def coupon(request):
   
    if Cart.coupon:
        coupon_shows =Coupon.objects.all()
    
    return render(request,'admindashboard/coupon.html',{'coupon_shows':coupon_shows})



def add_coupon(request):
    coupon = Coupon.objects.all()
    context = {
        'coupon': coupon
    }
    if request.method == 'POST':
        coupon_code = request.POST['coupon_code']
        discount_price = request.POST['discount_price']
        minimum_amount = request.POST['minimum_amount']
        end_date = request.POST['end_date']
        is_expired = 'is_expired' in request.POST

        existing_coupon = Coupon.objects.filter(Coupon_code=coupon_code).first()

        if existing_coupon:
            return render(request, 'admindashboard/edit_coupon.html', context={'error_message': 'Coupon with this code already exists.'})
        else:
            Coupon.objects.create(
                Coupon_code=coupon_code,
                discount_price=discount_price,
                minimum_amount=minimum_amount,
                is_expired=is_expired,
                end_date=end_date 
            )
        return redirect('coupon')

    return render(request, 'admindashboard/edit_coupon.html', context)


def edit_coupon(request, coupon_id):
    try:
        coupon = Coupon.objects.get(id=coupon_id)
    except Coupon.DoesNotExist:
        return render(request, 'admindashboard/edit_coupon.html', context={'error_message': 'Coupon not found.'})

    if request.method == 'POST':
        coupon_code = request.POST['coupon_code']
        discount_price = request.POST['discount_price']
        minimum_amount = request.POST['minimum_amount']
        end_date = request.POST['end_date']
        is_expired = 'is_expired' in request.POST

        # Check if the edited coupon code already exists, excluding the current coupon being edited.
        existing_coupon = Coupon.objects.filter(Coupon_code=coupon_code).exclude(id=coupon.id).first()

        if existing_coupon:
            return render(request, 'admindashboard/edit_coupon.html', context={'error_message': 'Coupon with this code already exists.'})
        else:
            # Update the coupon with the new values.
            coupon.Coupon_code = coupon_code
            coupon.discount_price = discount_price
            coupon.minimum_amount = minimum_amount
            coupon.is_expired = is_expired
            coupon.end_date = end_date 
            coupon.save()

        return redirect('coupon')

    context = {
        'coupon': coupon
    }
    return render(request, 'admindashboard/edit_coupon.html', context)





def delete_coupon(request,coupon_id):
    coupon_obj = Coupon.objects.get(id=coupon_id)
    coupon_obj.delete()
    
    return redirect('coupon')
