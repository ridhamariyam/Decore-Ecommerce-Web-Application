
import razorpay
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import render

def initiate_payment(request):
    if request.method == "POST":
        amount = int(request.POST["amount"]) * 100  # Amount in paise

        client = razorpay.Client(auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET))

        payment_data = {
            "amount": amount,
            "currency": "INR",
            "receipt": "order_receipt",
            "notes": {
                "email": "user_email@example.com",
            },
        }

        order = client.order.create(data=payment_data)
        
        # Include key, name, description, and image in the JSON response
        response_data = {
            "id": order["id"],
            "amount": order["amount"],
            "currency": order["currency"],
            "key": settings.RAZORPAY_API_KEY,
            "name": "Decore.",
            "description": "Payment for Your Product",
          
        }
        
        return JsonResponse(response_data)
    
    return render(request, "payment.html")


def payment_success(request):
    
    return render(request, "userside/payment/payment_success.html")

def payment_failed(request):
    return render(request, "payment_failed.html")