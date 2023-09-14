from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.conf import settings


# Create your models here.



class OTP(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    otp = models.CharField(max_length=4)

class Account(AbstractUser):
    phone_number = models.CharField(max_length=50,blank=True,null=True)
    is_block = models.BooleanField(default=False)
    user_token = models.UUIDField(default=uuid.uuid4,editable=False)
    refferal_code = models.IntegerField(blank=True, null=True)
    refferal_code1 =models.CharField(max_length=100,blank=True, null=True)
    refferal_link =  models.CharField(max_length=100,blank=True, null=True)

    def __str__(self):
        return self.username
    
    class Meta:
        verbose_name = 'Account'
        verbose_name_plural = 'Accounts'

      
class Address(models.Model):
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=200,null=True)
    phone_number = models.CharField(max_length=15,null=True)
    pincode = models.CharField(max_length=15,null=True)
    city = models.CharField(max_length=100,null=True)
    state = models.CharField(max_length=100,null=True)
    building_name = models.CharField(max_length=100,null=True)
    street_name = models.CharField(max_length=100,null=True)
    landmark = models.CharField(max_length=100,null=True)

    class Meta:
        verbose_name = 'Address'
        verbose_name_plural = 'Addresses'

# =====================================================Wallet=================================

class Wallet(models.Model):
    userr = models.OneToOneField(Account, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    

class Referral(models.Model):
    referrer = models.ForeignKey(Account, related_name='referrals', on_delete=models.CASCADE)
    referee = models.ForeignKey(Account, related_name='referred_by', on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    amount_credited = models.BooleanField(default=False)  # To track if the amount is credited

    



