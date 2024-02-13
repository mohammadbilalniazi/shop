from email.policy import default
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.utils import timezone
from django.db.models.signals import pre_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from products.models import Product
#from django. 
class Customer(models.Model):
    name = models.CharField(max_length=50,unique=True,null=False, blank=False)
    tazkira = models.CharField(max_length=50,null=True, blank=True)
    contact=models.CharField(max_length=50,null=True, blank=True)
    #added_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True) 
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Customer"


class Supplier(models.Model):
    name = models.CharField(max_length=50,unique=True,null=False, blank=False)
    tazkira = models.CharField(max_length=50,null=True, blank=True)
    contact=models.CharField(max_length=50,null=True, blank=True)
    #added_by = models.ForeignKey(User,on_delete=models.SET_NULL, null=True, blank=True) 
    def __str__(self):
        return f"{self.name}"

    class Meta:
        verbose_name_plural = "Supplier"


class Supplier_Ledger(models.Model):###supplier kahata
    supplier=models.ForeignKey(Supplier,on_delete=models.DO_NOTHING)
    creator_kahatha=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    #account_type=models.CharField(max_length=20,choices=ACCOUNT_TYPES)
    debit=models.IntegerField()  
    credit=models.IntegerField()  
    narration=models.CharField(max_length=80)        
    transation_date=models.CharField(max_length=80)          #transaction_date
 
    def __str__(self):
        return f"{self.customer}"
    verbose_name_plural = "Supplier Ledger"

ACCOUNT_TYPES=(("asset","asset"),("expense","expense"),("liability","liability"),("revenue","revenue"),("capital","capital"))
TRANS_TYPES=(("debit","debit"),("credit","credit"))


class Customer_Ledger(models.Model): # customer_kahatha
    customer=models.ForeignKey(Customer,on_delete=models.DO_NOTHING)
    creator_kahatha=models.ForeignKey(User,on_delete=models.DO_NOTHING)
    #account_type=models.CharField(max_length=20,choices=ACCOUNT_TYPES)
    debit=models.IntegerField()  
    credit=models.IntegerField()  
    narration=models.CharField(max_length=80)        
    transation_date=models.CharField(max_length=80)          #transaction_date

    
    def __str__(self):
        return f"{self.customer}"
    verbose_name_plural = "Customer Ledger"




class Log(models.Model):
    log_type = models.CharField(max_length=200)
    log_table=models.CharField(max_length=30)
    log_detail =models.TextField()
    log_date=models.CharField(max_length=40)
    logger=models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.log_type},{self.log_table}"
    
    class Meta:
        verbose_name_plural="Log"



class Sale_bill(models.Model):        #sale_bill = sale_detail
    payment=models.IntegerField()
    sale_date=models.DateField()
    vendor=models.ForeignKey(User,on_delete=models.DO_NOTHING,max_length=30)
    customer = models.ForeignKey(Customer,on_delete=models.DO_NOTHING,to_field='name',null=True, blank=True)
    total_sale_bill=models.IntegerField()
    discount=models.IntegerField(default=0)  
    def __str__(self):
        return f"{self.vendor}"
    
    verbose_name_plural = " Sale bill"


class Sales_detail(models.Model):
    sale_bill=models.ForeignKey(Sale_bill,on_delete=models.CASCADE)
    product=models.ForeignKey(Product,on_delete=models.DO_NOTHING,null=True,blank=True)
    item_amount=models.IntegerField(null=True,blank=True)              
    item_price=models.IntegerField()
    return_qty=models.IntegerField(null=True,blank=True)

    def __str__(self):
        return f"{self.item_name}{self} "    
    verbose_name_plural = "Sales Detail "


class Roznamcha(models.Model):
    spender=models.CharField(max_length=30)
    total_spent = models.IntegerField()
    detail=models.CharField(null=False,blank=False,max_length=30)
    date=models.DateField() 
       
    def __str__(self):
        return f"{self.detail}"
    
    verbose_name_plural = "Journal Voucher"


class Asset(models.Model):
    initial_asset=models.IntegerField()
    current_asset=models.IntegerField()
    start_date=models.DateField()
    def __str__(self):
        return f"{self.initial_asset} {self.current_asset}" 

    class Meta:
        verbose_name_plural="Asset"
    


# @receiver(pre_save, sender=Selling)
# def default_debit(sender, instance, **kwargs):
#     if not instance.debit:
#         instance.debit=instance.debit_initial()