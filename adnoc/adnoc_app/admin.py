from django.contrib import admin
from .models import *


class AdnocAdmin(admin.ModelAdmin):
    list_display = ('mobile_number','username','refered_by')

class UserRechargeAdmin(admin.ModelAdmin):
    list_display = ('id','user_id','recharge_date','transaction_id','is_valid','recharge_amount','is_credited')

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('id','prod_id','prod_id','purchase_date','transaction_id','is_approved')

class WithdrawRequestAdmin(admin.ModelAdmin):
    list_display = ('id','amount','request_date','acc_name','acc_no','ifsc','mobile_number','status','user_id')


# Register your models here.
admin.site.register(OTP)
admin.site.register(AdnocUser,AdnocAdmin)
admin.site.register(Product)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(WalletHistory)
admin.site.register(WithdrawRequest, WithdrawRequestAdmin)
admin.site.register(UserRecharge, UserRechargeAdmin)
admin.site.register(transactions)
admin.site.register(userBank)