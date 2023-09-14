from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Account,Address
from .models import OTP
# Register your models here.

class AccountAdmin(UserAdmin):
    list_display = ('email','first_name','last_name','username','last_login')

    filter_horizontal = ()
    list_filter =()
    fieldsets =()


admin.site.register(Account,AccountAdmin)
admin.site.register(Address)
admin.site.register(OTP)