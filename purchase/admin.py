from django.contrib import admin
# Register your models here.        
from purchase.models import Bill,Bill_detail,Purchaser
@admin.register(Bill)
class BillAdmin(admin.ModelAdmin):
    #list_display=("item_name","item_amount","item_price","date","return_qty")
    #list_display=get_model_fields(Bill)
    list_display=("organization","bill_no")
    
@admin.register(Bill_detail)
class Bill_detailAdmin(admin.ModelAdmin):
    list_display=("bill","product","unit","item_amount","item_price","return_qty")
    
# @admin.register(Purchaser)
class PurchaserAdmin(admin.ModelAdmin):
    list_display=("name","user")
     
