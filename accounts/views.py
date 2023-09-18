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
from .models import OTP,Referral,Wallet
from django.shortcuts import get_object_or_404
from accounts.models import Account,Wallet,Referral
from django.contrib.sessions.models import Session
from django.contrib.auth import update_session_auth_hash
from accounts.models import Address
from accounts.models import Account,Address
from django.contrib import messages
from xhtml2pdf import pisa
from order.models import Order,Order_product
import os
from django.template.loader import render_to_string
import random,re
import string



def generate_referral_code_and_signup_link(user, request):
    # Get the first three letters of the user's name (or the entire name if it's shorter)
    user_name = user.username  # Assuming the username field stores the user's name
    name_prefix = user_name[:3].upper()
    
    # Generate the remaining characters for the code
    code_length = 6  # You can adjust the length as needed
    random_characters = ''.join(random.choices(string.ascii_uppercase + string.digits, k=code_length - len(name_prefix)))
    referral_code = name_prefix + random_characters
    
    # Construct the signup link with the referral code
    signup_link = f'/register/?ref={referral_code}'  # Update the URL path as needed

    # Save the referral code and link to the user's profile
    user.refferal_code1 = referral_code
    user.refferal_link = signup_link
    user.save()
    
    return redirect('profile')




def profile(request):
    # user = request.user
    # if user.refferal_code1:
    #    referral_code = user.refferal_code1
    # else:
    #     referral_code = False

    # if user.refferal_link:
    #    signup_link = user.refferal_link
    # else:
    #     signup_link = False   

    # context = {'ref_link': signup_link, 'ref_code': referral_code}

    return render(request, 'userside/profile.html')



def myaccount(request):
    return render(request, 'userside/myaccount.html')




# =============================================ADDRESS=============================================

def address(request):
    user_addresses = Address.objects.filter(user=request.user)
    return render(request, 'userside/address.html', {'user_addresses': user_addresses})
  

def add_address(request):
    if request.method == 'POST':
        fullname = request.POST.get('fullname')
        phone_number = request.POST.get('phone_number')
        pincode = request.POST.get('pincode')
        city = request.POST.get('city')
        state = request.POST.get('state')
        building_name = request.POST.get('building_name')
        street_name = request.POST.get('street_name')
        landmark = request.POST.get('landmark')

        user = request.user

        address = Address(user=user, full_name=fullname, phone_number=phone_number, pincode=pincode, city=city,
                          state=state, building_name=building_name, street_name=street_name, landmark=landmark)
        address.save()
        messages.success(request, 'Address added successfully')

        return redirect('address')

    return render(request, 'userside/address.html')


def update_address(request, address_id):
    address = Address.objects.get(id=address_id)
    print('ffffffffffffffffffffffffff', address)

    if request.method == 'POST':
        # Get the new values for all fields from the request.POST data
        new_full_name = request.POST.get('fullname')
        new_phone_number = request.POST.get('phone_number')
        new_pincode = request.POST.get('pincode')
        new_city = request.POST.get('city')
        new_state = request.POST.get('state')
        new_building_name = request.POST.get('building_name')
        new_street_name = request.POST.get('street_name')
        new_landmark = request.POST.get('landmark')

        # Update all fields and save the address
        address.full_name = new_full_name
        address.phone_number = new_phone_number
        address.pincode = new_pincode
        address.city = new_city
        address.state = new_state
        address.building_name = new_building_name
        address.street_name = new_street_name
        address.landmark = new_landmark
        address.save()

        return redirect('address')  # Redirect to a page showing the updated address

    return render(request, 'userside/update_address.html', {'address': address})


def delete_address(request, address_id):
    address = get_object_or_404(Address, id=address_id, user=request.user)

    if request.method == 'POST':
        address.delete()
        return  redirect('address')
    else:
        return  redirect('address')

    # This part is not reachable after the return statements above
    return render(request, 'userside/update_address.html', {'address': address})
    


def otp(request):
    if request.user.is_authenticated:
        
        return redirect('login') 


@cache_control(no_cache=True,must_revalidate=True,no_store=True)
def handlelogin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_block:
                messages.error(request, 'You are not able to login')
                return redirect(handlelogin)
            
            if request.POST.get('remember_me'):
                response = redirect('home')
                response.set_cookie('user_token', user.user_token, max_age=24 * 60 * 60)  
                return response

            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Username or password is incorrect!')

    return render(request, 'userside/login.html')




def register(request):
    referral_code = request.GET.get('ref')
    if request.method == 'POST':
        get_otp = request.POST.get('otp')
        if get_otp:
            get_email = request.POST.get('email')
            user = Account.objects.get(email=get_email)
            if get_otp == OTP.objects.filter(user=user).first().otp:
                user.is_active = True
                user.save()
                messages.success(request, f'Account is created for {user.email}')
                OTP.objects.filter(user=user).delete()
                return redirect(handlelogin)
            else:
                messages.warning(request, 'You Entered a wrong OTP')
                return render(request, 'userside/otp.html')

        else:
            username = request.POST.get('username')
            email = request.POST.get('email')
            password1 = request.POST.get('password1')
            password2 = request.POST.get('password2')

            if password1 != password2:
                messages.error(request, "Passwords do not match.")
                return render(request, 'userside/register.html')
            
            if len(password1) < 6:
                messages.error(request, "Password should be at least 6 characters long.")
                return render(request, 'userside/register.html')    
            
            if not re.search(r'[a-zA-Z]', password1) or not re.search(r'\d', password1):
                messages.error(request, "Password must contain at least one alphabet character and one number.")
                return render(request, 'userside/register.html')

            if not username.isalpha():
                messages.error(request, "Username should only contain alphabetical characters.")
                return render(request, 'userside/register.html')

            if ' ' in username:
                messages.error(request, 'Username should not contain spaces')
                return render(request, 'userside/register.html')

            if Account.objects.filter(username=username).exists():
                messages.error(request, 'Username already taken')
                return render(request, 'userside/register.html')

            if Account.objects.filter(email=email).exists():
                messages.error(request, 'Email already taken')
                return render(request, 'userside/register.html')

            my_user = Account.objects.create_user(username, email, password1)
            my_user.is_active = False
            my_user.save()

            otp = int(random.randint(1000, 9999))
            otp_instance = OTP(user=my_user, otp=otp)
            otp_instance.save()

            send_mail(
                "Mobile Login OTP.",
                f"Your otp for verifying mobile number is : {otp}",
                settings.EMAIL_HOST_USER,
                [my_user.email],
                fail_silently=False
            )

            # Check if there's a referral code in the query parameters
            print("helooooooooooooooooooooooooooooooooooooooooooooooooooooooooo")
            
            print(referral_code)
            if referral_code:
                referrer_user = Account.objects.get(refferal_code1=referral_code)
                bonus_amount = 50
                print(referrer_user)
                # Retrieve or create the Wallet object associated with the user
                wallet, created = Wallet.objects.get_or_create(userr=referrer_user)
                if wallet:
                   wallet.balance += bonus_amount
                   wallet.save()
                if created:
                   created.balance += bonus_amount
                   created.save()   

            return render(request, 'userside/otp.html', {'email': my_user.email, 'user': my_user})

    if request.user.is_authenticated:
        return redirect('home')

    return render(request, 'userside/register.html',{'referral_code':referral_code})


def changepassword(request):
    if request.method == 'POST':
        new_username = request.POST['username']
        new_firstname = request.POST['first_name']
        new_lastname = request.POST['last_name']
        new_phonenumber = request.POST['phone_number']

        if (
            new_username != request.user.username
            or new_firstname != request.user.first_name
            or new_lastname != request.user.last_name
            or new_phonenumber != request.user.phone_number
        ):
            request.user.username = new_username
            request.user.first_name = new_firstname
            request.user.last_name = new_lastname
            request.user.phone_number = new_phonenumber
            request.user.save()
            messages.success(request, 'Profile updated successfully')

        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        if current_password and new_password == confirm_password:
            if request.user.check_password(current_password):
                request.user.set_password(new_password)
                request.user.save()
                update_session_auth_hash(request, request.user)
                messages.success(request, 'Password changed successfully')
            else:
                messages.error(request, 'Current password is incorrect')
        elif new_password != confirm_password:
            messages.error(request, 'New passwords do not match')

        return redirect('profile')
    else:
        return render(request, 'userside/profile.html')

def generate_invoice_pdf(order):
    # Render the invoice template to a string
    order_items = Order_product.objects.filter(order=order)
    invoice_html = render_to_string('userside/order_invoice.html', {'order': order,'order_items':order_items})
    # print(invoice_html)

    # Create a temporary file path to save the PDF
    temp_file_path = os.path.join(settings.MEDIA_ROOT, 'temp_invoice.pdf')
    # print(temp_file_path)

    # Generate the PDF using xhtml2pdf
    with open(temp_file_path, 'w+b') as file:
        pisa.CreatePDF(invoice_html, dest=file)
  

    return temp_file_path



# function to download order invoice.
def download_invoice(request, order_id):
    order = Order.objects.get(id=order_id)
    print('--------------------------------',order)
    invoice_path = generate_invoice_pdf(order)

    if invoice_path:
        # Open the generated PDF file in binary mode
        with open(invoice_path, 'rb') as file:
            response = HttpResponse(file.read(), content_type='application/pdf')
            response['Content-Disposition'] = f'attachment; filename="RR-order-invoice-{order_id}.pdf"'

        # Delete the temporary invoice file
        os.remove(invoice_path)

        return response

    return HttpResponse('Failed to generate the invoice', status=500)



# =========================wallet======================

def wallet(request):
    user = request.user  # Assuming you have user authentication in place
    
    try:
        wallet = Wallet.objects.get(userr=user)
    except Wallet.DoesNotExist:
        # Create a new wallet if it doesn't exist for the user
        wallet = Wallet.objects.create(userr=user, balance=0.00)
    
    # Check if the user has any completed but uncredited referrals
    uncredited_referrals = Referral.objects.filter(referee=user, completed=True, amount_credited=False)
    
    if uncredited_referrals.exists():
        # Calculate the total referral reward amount
        total_reward_amount = uncredited_referrals.count() * 50
        
        # Split the reward between referee and referrer
        referee_share = total_reward_amount / 2
        referrer_share = total_reward_amount / 2
        
        # Update the wallet balances
        wallet.balance += referee_share
        wallet.save()
        
        referrer = uncredited_referrals.first().referrer
        referrer_wallet = Wallet.objects.get(userr=referrer)
        referrer_wallet.balance += referrer_share
        referrer_wallet.save()
        
        # Mark the referral rewards as credited
        
        uncredited_referrals.update(amount_credited=True)

        
    
    return render(request, 'userside/wallet.html', {'wallet': wallet,'uncredited_referrals':uncredited_referrals})
