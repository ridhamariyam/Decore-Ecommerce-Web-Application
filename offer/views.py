from django.shortcuts import render, redirect
from .models import Offer
from cart.models import Coupon
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from store.models import Product

# Create your views here.

# for adding a new offer
@login_required(login_url='user_login')
def adminoffer(request):

    offer = Offer.objects.filter(is_deleted=False)
    context = {
        'offers': offer,
    }

    return render(request,'admindashboard/offer.html',context)



@login_required(login_url='user_login')
def add_offer(request):
    if request.method == 'POST':
        # Retrieve form data
        offer_name = request.POST['offer_name']
        discount_percentage = request.POST['discount_percentage']
        start_date = request.POST['start_date']
        end_date = request.POST['end_date']

        # Create a new offer object
        offer = Offer.objects.create(
            title=offer_name,
            discount_percentage=discount_percentage,
            start_date=start_date,
            end_date=end_date
        )

        # Save the offer to the database
        offer.save()

        # Redirect to a offer page
        return redirect('adminoffer')  
        
    return render(request, 'admindashboard/add_offer.html')


def remove_offer(request,offer_id):
    offer = Offer.objects.get(id=offer_id).delete()
    messages.warning(request,'Offer has been removed successfully.')
    return redirect('adminoffer')


def apply_offer(request):
    if request.method == 'POST':
        selected_offer_id = request.POST.get('selected_offer')
        product_id = request.POST.get('product_id')

        try:
            selected_offer = Offer.objects.get(id=selected_offer_id)
            product = Product.objects.get(id=product_id)

            # Implement your logic here to update the product based on the selected offer
            # For example, you can update the product's price and discount percentage:
            product.price = product.price * (1 - selected_offer.discount_percentage / 100)
            product.offer = selected_offer  # Save the selected offer for reference
            product.save()

            return redirect('adminproduct')  # Redirect to the product detail page
        except (Offer.DoesNotExist, Product.DoesNotExist):
            # Handle any errors here
            pass

    # Handle GET request or errors
    return render(request, 'admindashboard/productadmin.html')




# def refer_friend(request):
#     if request.user.is_authenticated:
#         # Check if the referral has already been completed by this user
#         if not Referral.objects.filter(referrer=request.user).exists():
#             # Create a referral object for the referrer
#             referrer_referral = Referral(referrer=request.user, referee=None, completed=False)
#             referrer_referral.save()

#             # Update the referrer's wallet
#             referrer_wallet, created = Wallet.objects.get_or_create(user=request.user)
#             referrer_wallet.balance += Decimal('50.00')
#             referrer_wallet.save()

#             # Check if a referral link was provided in the request
#             referee_id = request.GET.get('referral', None)
#             if referee_id:
#                 try:
                  
#                     referee = User.objects.get(id=referee_id)

                   
#                     referee_referral = Referral(referrer=referrer_wallet.user, referee=referee, completed=True)
#                     referee_referral.save()

                   
#                     referee_wallet, created = Wallet.objects.get_or_create(user=referee)
#                     referee_wallet.balance += Decimal('50.00')
#                     referee_wallet.save()
#                 except User.DoesNotExist:
#                     pass

            
#             return render(request, 'referral.html', {'referral_link': referral_link, 'balance': referrer_wallet.balance})
#     return redirect('login')  
