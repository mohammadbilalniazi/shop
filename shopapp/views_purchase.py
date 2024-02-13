from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from django.urls import reverse
from django.template import loader 
from django.contrib.auth.decorators import login_required
from shopapp.models import Customer, Supplier , Supplier_Ledger , Customer_Ledger , Log ,Bill, Bill_detail,Sale_bill,Sales_detail,Roznamcha,Asset
from products.models import Product
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages

@login_required(login_url='/admin')
def purchase_show(request,bill_id=None):
    context={}
    if bill_id==None:
        context['bills']=Bill.objects.all()
        template=loader.get_template('purchase_show.html')
    else:
        #bill.objects.get(id=int(bill_id))
        print(Bill.objects.get(id=int(bill_id)))
        #return HttpResponse(bill.objects.get(id=int(bill_id)))
        context['detail']=True
        bill_obj=Bill.objects.get(id=int(bill_id))
        print("bill_obj.payment=",bill_obj.payment)
        context['bill']=bill_obj
        template=loader.get_template('purchase_temp.html')
    
    
    return HttpResponse(template.render(context,request))

@login_required(login_url='/admin')
def Bill_form(request):  
    #print("dkdk",request.POST)
    print(request.POST)
    print("request.method 2",request.method)
    print("item_name=",request.POST.getlist("item_name"), " len(request.POST.getlist('item_name'))=",len(request.POST.getlist("item_name")))
    print("item_amount=",request.POST.getlist("item_amount")," len(request.POST.getlist('item_amount)=",len(request.POST.getlist("item_amount")))
    print("item_price=",request.POST.getlist("item_price"))
    print("return_qty=",request.POST.getlist("return_qty"))
    context={}    
    if request.method == "POST":
        #print(request.GET)
        ########################################## bill input taking############################
        bill=request.POST.get("bill_no",None)
        ##date conversion##
        date=request.POST.get("bill_date",None)
        date=datetime.strptime(date,"%Y-%m-%d")
        ###################
        vendor=request.POST.get("company",None)
        creator=request.POST.get("creator",None)
        creator=request.user
        total=request.POST.get("total",None)
        payment=request.POST.get("total_paymen5",None)
        bill_obj=Bill(date=date,vendor=vendor,creator=creator,total=total,payment=payment)
        bill_obj.save()
        ######################################################bill detail############################

        product=request.POST.getlist('item_name',None)        #in models it's name is product
        print("test")
        item_amount=request.POST.getlist('item_amount',None)
        
        item_price=request.POST.getlist('item_price',None)

        return_qty=request.POST.getlist('return_qty',None)
        ########################################validations##################################
        ########################validation 1 if charger1 is repeated 2 times than reject##############
        ######################## validations 2 if return_qty>item_amount##################reject
        ######################## if item_name total_amount is < payment and payment is more then reject ############ 
        for i in range(len(request.POST.getlist('item_name'))):
            print(product[i]," ",item_amount[i])
            #return HttpResponse(Product.objects.get(item_name=product[i]))
            product_obj=Product.objects.get(item_name=product[i])
            purchase_detail_obj=Bill_detail(bill=bill_obj,product=product_obj,item_amount=item_amount[i],item_price=item_price[i],return_qty=return_qty[i])
            purchase_detail_obj.save()
        #template=loader.get_template('purchase_temp.html')
        #return HttpResponse(request.POST)
    else:
        print("test2")   #return HttpResponse(request.POST)
      
        #return HttpResponse(User.objects.all())
        context={
            'users':User.objects.all(),
        } 

    template=loader.get_template('purchase_temp.html')
    return HttpResponse(template.render(context,request))
  