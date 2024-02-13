from django.db.models import Sum
from django.http import HttpResponse
from jalali_date import date2jalali
from django.template import loader  
from django.contrib.auth.decorators import login_required
from products.models import Product,Unit,Store
from products.views_product import change_detail_price_product,handle_product_for_bill_rcvr_org
from common.organization import findOrganization
from common.date import handle_day_out_of_range
from configuration.models import Organization
from configuration.models import *
from django.contrib.auth.models import User
from datetime import datetime
from django.contrib import messages
from .models import Bill, Bill_detail,Bill_Description,Purchaser,Bill_Receiver
from django.forms.models import model_to_dict
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .forms import Bill_Form
from django.db.models import Q,Max
from .serializer import Bill_search_Serializer
import re
import json

def getBillNo(request,organization_id,bill_rcvr_org_id,bill_type=None):
    date = date2jalali(datetime.now()) 
    year=date.strftime('%Y')
    (self_organization,parent_organization)=findOrganization(request,organization_id)
    print("self_organization , parent_organization ",self_organization,parent_organization)
    (bill_rcvr_org,parent_bill_rcvr_org)=findOrganization(request,bill_rcvr_org_id)
    opposit_bill=get_opposit_bill(bill_type)
    if bill_type=="EXPENSE":
        bill_query=Bill.objects.filter(year=int(year),bill_type=bill_type,organization=parent_organization)
    else:    
        bill_query=Bill.objects.filter(Q(year=int(year)),Q(Q(bill_type=bill_type),Q(organization=parent_organization),Q(bill_receiver__bill_rcvr_org=parent_bill_rcvr_org)) | Q(Q(bill_type=opposit_bill),Q(bill_receiver__bill_rcvr_org=parent_bill_rcvr_org),Q(organization=parent_organization)))

    if bill_query.count()>0:  
        bill=bill_query[0] 
        bill_no=bill_query.aggregate(Max('bill_no'))['bill_no__max']+1
    else:
        bill_no=1
    return bill_no
    

@api_view(("GET",))
def select_bill_no(request,organization_id,bill_rcvr_org_id,bill_type=None):
    return Response({"bill_no":getBillNo(request,organization_id,bill_rcvr_org_id,bill_type)})

@login_required(login_url='/admin')
def bill_show(request,bill_id=None):
    # print("bill_id =",bill_id)
    context={}
    form=Bill_Form()
    context['form']=form
    (self_organization,parent_organization)=findOrganization(request)
    if bill_id==None :
        context['bills']=Bill.objects.all().order_by("-pk")
        context['rcvr_orgs']=Organization.objects.all() 
        template=loader.get_template('bill/bill_show.html')
    else:
        # context['detail_flag']=True
        bill_obj=Bill.objects.get(id=int(bill_id))
        form.fields['date'].initial=str(bill_obj.date) #before  hawala.mustharadi_file
        context['bill']=bill_obj
        context['products']=Product.objects.filter(organization=bill_obj.organization)
        context['units']=Unit.objects.all()
        if bill_obj.organization==parent_organization:                 
            context['rcvr_orgs']=Organization.objects.all()     
        elif bill_obj.bill_receiver.bill_rcvr_org==parent_organization:

            context['rcvr_orgs']=Organization.objects.filter(id=parent_organization.id)
        if bill_obj.bill_type!="EXPENSE":
            store_query=Store.objects.filter(Q(organization=bill_obj.organization) | Q(organization=bill_obj.bill_receiver.bill_rcvr_org))
        else:
            store_query=Store.objects.filter(organization=bill_obj.organization)
        print("store_query ",store_query)
        context['stores']=store_query
        template=loader.get_template('bill/bill_form.html')
        # return HttpResponse("test")
    print('(self_organization,parent_organization) ',self_organization,' ',parent_organization)
    context['organization']=parent_organization
    return HttpResponse(template.render(context,request))

@login_required(login_url='/admin')
def bill_delete(request,id=None):
    context={}
    self_organization,parent_organization=findOrganization(request)
    if id!=None:
        context['detail']=True
        bill_query=Bill.objects.filter(id=int(id))
        if bill_query.count()>0:
            bill_obj=bill_query[0]
            if bill_obj.organization!=parent_organization:
                message="The Organization {} can not delete the bill id {} because it is not creator of bill".format(parent_organization.name,id)
                messages.error(request,message=message)
                return bill_show(request,bill_id=id)
            if hasattr(bill_obj,'bill_receiver'):
                if bill_obj.bill_receiver.approval_user!=None or bill_obj.bill_receiver.is_approved: # it means approved
                    message="Bill Id {} is can not be deleted it is already approved".format(id)
                    messages.error(request,message=message)
                    return bill_show(request,bill_id=id)
            bill_details=bill_obj.bill_detail_set.all()
            for bill_detail in bill_details:
                try: # should be reducred from the opposit here bill_rcvr
                    if bill_obj.bill_type=='PURCHASE' or bill_obj.bill_type=='SELLING':
                        bill_rcvr_org=bill_obj.bill_receiver.bill_rcvr_org
                        (bill_detail,price_changed,detail_changed)=change_detail_price_product(bill_detail,'DELETE',bill_rcvr_org)
                except Exception as e:
                    print("product_detail_bill_rcvr_org $ e",e) 
            bill_obj.delete()
            message="Bill Id {} is Successfully deleted".format(id)
            messages.success(request,message=message)
        else:
            message="Bill Id {} Not Present".format(id)
            messages.error(request,message=message)
    else:
        message="Bill Id Not Present"
        messages.error(request,message=message)
    return bill_show(request,bill_id=None)

@login_required(login_url='/admin')
@api_view(['GET','DELETE'])
def bill_detail_delete(request,bill_detail_id=None):
    context={} 
    self_organization,parent_organization=findOrganization(request)
    message=""
    is_success=False
    if bill_detail_id!=None:
        context['detail']=True
        bill_detail_query=Bill_detail.objects.filter(id=int(bill_detail_id))
        if bill_detail_query.count()>0:      
            bill_detail=bill_detail_query[0]
            bill=bill_detail.bill
            if bill.organization!=parent_organization:
                message="The Organization {} can not delete the bill id {} because it is not creator of bill".format(parent_organization.name,id)
                return Response({"Message":message,"is_success":False})
            if bill.bill_receiver.approval_user!=None: # it means approved
                return Response({"Message":'it is approved',"is_success":False})
            if len(bill.bill_detail_set.all())==1:
                bill_delete(request,int(bill.id))
            if bill.bill_type!='EXPENSE':
                bill_rcvr_org=bill.bill_receiver.bill_rcvr_org

            deleted_amount=(previous_item_amount-previous_return_qty)*item_price
            total=bill.total
            remaining=total-deleted_amount

            try:
                bill_detail.delete()
                bill.total=remaining
                bill.save()
                if bill.bill_type=='PURCHASE' or bill.bill_type=='SELLING':
                    (bill_detail,price_changed,detail_changed)=change_detail_price_product(bill_detail,'DELETE',bill_rcvr_org)

                message="Bill Detail Id {} is Successfully deleted and deleted amount {} and current total bill amount is {}".format(bill_detail_id,deleted_amount)
            except Exception as e:
                message=str(e)
            # message="Bill Detail Id {} is Successfully deleted and deleted amount {} and current total bill amount is {}".format(bill_detail_id,deleted_amount)
            # status=status.HTTP_200_OK            
            print("message ",message)
            is_success=True
            messages.success(request,message=message)
        else:
            message="Bill Detail Id {} is not deleted".format(bill_detail_id)
            messages.error(request,message=message)
            # status=status.HTTP_204_NO_CONTENT
            print("message ",message)
            is_success=False
    return Response({"Message":message,"is_success":is_success})

@login_required(login_url='/admin')
def Bill_form(request):
    template=loader.get_template('bill/bill_form.html')
    #return HttpResponse(User.objects.all())    
    # date=pytz.timezone("Asia/Kabul").localize(datetime.now()).strftime('%Y-%m-%d')
    date = date2jalali(datetime.now())
    year=date.strftime('%Y')
    self_organization,parent_organization=findOrganization(request)
    # print('self_organization ',self_organization,' parent_organization ',parent_organization)
    # print('Store.objects.filter(organization=parent_organization) ',Store.objects.filter(organization=parent_organization))
    form=Bill_Form()
    context={}
    form.fields['date'].initial=date
    # bill_no=getBillNo(request,parent_organization.id,'PURCHASE')
    context={
        'form':form,
        'organization':parent_organization,
        # 'rcvr_orgs':Organizations.objects.all(),
        'stores':Store.objects.filter(organization=parent_organization),
        # 'bill_no':bill_no,
        'date':date,
    } 
    # print("context=",context)
    return HttpResponse(template.render(context,request))

def get_opposit_bill(bill_type):
    opposit_bills={"SELLING":"PURCHASE","PURCHASE":"SELLING","PAYMENT":"RECEIVEMENT","RECEIVEMENT":"PAYMENT","EXPENSE":"EXPENSE"}
    return opposit_bills[bill_type]

def handle_profit_loss(bill_detail_obj,amount,operation='INCREASE'):
    bill=bill_detail_obj.bill
    if operation=='INCREASE':
        bill_detail_obj.profit=bill_detail_obj.profit+amount
        bill.profit=bill.profit+amount
    else:
        bill_detail_obj.profilt=bill_detail_obj.profit-amount
        bill.profilt=bill.profit-amount
    try:
        bill_detail_obj.save()
        bill.save()
        ok=True
    except Exception as e:
        ok=False    
    return ok

@login_required(login_url='/admin')
@api_view(['POST','PUT'])
def Bill_insert(request):  
    context={}    
    print(".request.data ",request.data)
    ########################################## Bill input taking############################
  
    bill_no=int(request.data.get("bill_no",None))  
    id=request.data.get("id")
    date_str=request.data.get("date")
    try:
        date=datetime.strptime(date_str,'%Y-%m-%d')
    except Exception as e:
        if str(e)=="day is out of range for month":
            date_str=handle_day_out_of_range(date_str)
            date=datetime.strptime(date_str,'%Y-%m-%d')
        else:
            return Response({"message":str(e),"ok":False})
    year=int(date.strftime('%Y'))
    status=int(request.data.get("status",0))
    ############before request.data  and request.data.getlist
    store=int(request.data.get("store",0))
    store_query=Store.objects.filter(id=store)
    
    bill_receiver_store=int(request.data.get("bill_receiver_store",0))
    bill_receiver_store_query=Store.objects.filter(id=bill_receiver_store)
    print("bill_receiver_store id",bill_receiver_store)
    if store_query.count()>0:
        store=store_query[0] 
    if bill_receiver_store_query.count()>0:
        bill_receiver_store=bill_receiver_store_query[0]
    # print("bill_receiver_store ",bill_receiver_store)
    # return Response({"message":"test","ok":False})
    organization=request.data.get("organization")
    organization=Organization.objects.get(id=int(organization))
    (self_organization,parent_organization)=findOrganization(request)

    bill_type=request.data.get("bill_type",None)
    creator=request.user
    total=request.data.get("total",0)
    if total=='' or total=="" or total==None:
        total=0
    payment=request.data.get("total_payment",0)      
    ###################bill_detail###############
    product=request.data.get('item_name',0)        #getlist=> get
    item_amount=request.data.get('item_amount',0)#getlist=> get
    unit=request.data.get('unit',None)#getlist=> get
    item_price=request.data.get('item_price',0)#getlist=> get
    return_qty=request.data.get('return_qty',0)#getlist=> get
    bill_detail_id=request.data.get('bill_detail_id',"")#getlist=> get
    ################## bill_receiver#######################
    bill_rcvr_org=request.data.get("bill_rcvr_org",None) #id
    try:
        bill_rcvr_org=Organization.objects.get(id=int(bill_rcvr_org))
    except Exception as e:
        return Response({"message":str(e),"ok":False,"data":None,"bill_id":None}) 
    prev_bill_rcvr_org=bill_rcvr_org #initially we take it as then we change in update if previous bill rcvr_org is different from current

    is_approved=request.data.get("is_approved",False)
    if is_approved==1 or is_approved=="1" or is_approved=="on":
        is_approved=True
    else:
        is_approved=False
    approval_date=request.data.get("approval_date",None)
    # print("approval_date ",approval_date)
    try:
        approval_date = date2jalali(datetime.now())
        approval_date=datetime.strptime(date.strftime('%Y-%m-%d'),'%Y-%m-%d')
    except Exception as e:
        date_str=str(date2jalali(datetime.now()))
        date_str=handle_day_out_of_range(date_str)
        approval_date=datetime.strptime(date_str,'%Y-%m-%d')
    
    # approval_user=request.data.get("approval_user")
    print("1status ",status," approval_date=",approval_date," is_approved= ",is_approved)
    if bill_rcvr_org==parent_organization:
        if is_approved or int(status)==1:
            status=1
            approval_user=request.user
            is_approved=True
        elif status==0:
            approval_user=None
            is_approved=False
        else:
            approval_user=request.user
            is_approved=False
    else:
        status=0
        approval_date=None
        approval_user=None
        is_approved=False
    print("2status ",status," approval_date=",approval_date," approval_user ",approval_user," is_approved= ",is_approved)
    # return Response({"message":'test',"ok":False})
    #########endof data prepration########
    if id!="" and id!='':
        ###############update#########################
        bill_query=Bill.objects.filter(id=int(id))
        bill_obj=bill_query[0] 
        print("update with id== something bill_query.count()==0 ",bill_query.count()==0) 
        if bill_query.count()==0:
            ok=False
            message="The Bill with Id {} not exist ".format(id)
            return Response({"message":message,"ok":ok})
    
        if hasattr(bill_obj,'bill_receiver'):
            if bill_obj.bill_receiver.approval_user!=None or bill_obj.bill_receiver.is_approved: # it means approved
                message="Bill Id {} is can not be updated it is already approved".format(id)
                ok=False
                return Response({"message":message,"ok":ok})
        # praint(dir(bill_obj))
        previous_bill_type =bill_obj.bill_type
        # print("0 bill_obj.bill_type ",bill_obj.bill_type," previous_bill_obj.bill_type ",previous_bill_obj.bill_type)  
        bill_obj.total=total
        bill_obj.payment=payment
        bill_obj.bill_type=bill_type
        bill_obj.profit=0
        # bill_obj.organization=organization   #because organization=findorganization in opposit organization approval will be changed
        ####################### bill_description update bill_receiver update####################
        if previous_bill_type!="EXPENSE":
            # bill_description=bill_obj.bill_description
            if hasattr(bill_obj,'bill_receiver'):
                bill_receiver=bill_obj.bill_receiver
                prev_bill_rcvr_org=bill_receiver.bill_rcvr_org
        if previous_bill_type!="EXPENSE" and bill_type=="EXPENSE":
            bill_receiver.delete()
            bill_description.delete()
    else: ############### new insert Bill if not in system#############
        opposit_bill=get_opposit_bill(bill_type)
        # bill_query=Bill.objects.filter(Q(bill_no=int(bill_no)),Q(year=year),Q(Q(bill_type=bill_type),Q(organization=organization)) | Q(Q(bill_type=opposit_bill),Q(bill_receiver__bill_rcvr_org=organization)))
        bill_query=Bill.objects.filter(Q(bill_no=int(bill_no)),Q(year=int(year)),Q(Q(bill_type=bill_type),Q(organization=organization),Q(bill_receiver__bill_rcvr_org=bill_rcvr_org)) | Q(Q(bill_type=opposit_bill),Q(bill_receiver__bill_rcvr_org=bill_rcvr_org),Q(organization=organization)))
        if bill_query.count()>0: # if we are not having update then we check if such bill present or not if exists we not enter
            ok=False
            message="The Bill is already in system search for Bill No {} Bill Type {} Year {} ".format(bill_no,bill_type,year)
            return Response({"message":message,"ok":ok})
        bill_obj=Bill(bill_type=bill_type,date=date,year=year,bill_no=bill_no,organization=organization,creator=creator,total=total,payment=payment)
    try:
        bill_obj.save()

        if bill_type!="EXPENSE":  # in expense we do not need bill_description and bill_receiver
            bill_description_query=Bill_Description.objects.filter(bill=bill_obj)
            bill_receiver_query=Bill_Receiver.objects.filter(bill=bill_obj)
            if bill_description_query.count()>0:
                bill_description_query.update(store=store,status=status)
            else:
                bill_description=Bill_Description(bill=bill_obj,store=store,status=status)
                bill_description.save()  
            if bill_receiver_query.count()>0:
                bill_receiver_query.update(bill_rcvr_org=bill_rcvr_org,is_approved=is_approved,approval_date=approval_date,approval_user=approval_user,store=bill_receiver_store)
            else:
                bill_receiver=Bill_Receiver(bill=bill_obj,bill_rcvr_org=bill_rcvr_org,is_approved=is_approved,approval_date=approval_date,approval_user=approval_user,store=bill_receiver_store)
                bill_receiver.save()  
        ok=True
        message="bill No {} Successfully Insert".format(bill_no)
    except Exception as e:
        ok=False
        message=str(e)
        print("e ",e)
        return Response({"message":message,"ok":ok})
    ######################## if item_name total_amount is < payment and payment is more then reject ############ 
    if bill_type=="PURCHASE" or bill_type=="SELLING":
        for i in range(len(product)):
            try:
                unit_obj=Unit.objects.get(id=unit[i])
                #current products 
                product_obj=Product.objects.get(id=product[i])
                product_of_bill_rcvr_org=handle_product_for_bill_rcvr_org(product_obj,bill_rcvr_org)
            
            except Exception as e:
                print("*****e=",str(e))
                return Response({"message":str(e),"ok":False})
                # return Response({"message":message,"ok":False})
            
            # print("product_of_bill_rcvr_org ",product_of_bill_rcvr_org)
         
            if bill_detail_id[i]=='':
                bill_detail_obj=Bill_detail(bill=bill_obj,product=product_obj,unit=unit_obj,item_amount=item_amount[i],item_price=item_price[i],return_qty=return_qty[i])     
                try:    

                    bill_detail_obj.save() 
                    if bill_type=='SELLING':
                        purchased_price=product_obj.purchased_price
                        amount=(item_price[i]-purchased_price)*(item_amount[i]-return_qty[i])
                        ok=handle_profit_loss(bill_obj,amount,operation='INCREASE')

                    (bill_detail,price_changed,detail_changed)=change_detail_price_product(bill_detail_obj,'INSERT',bill_rcvr_org) 
                    
                except Exception as e:
                    ok=False
                    message=str(e)
                    (bill_detail,price_changed,detail_changed)=change_detail_price_product(bill_detail_obj,'DELETE',bill_rcvr_org)    
                    print("e ",e)
            else:       
                bill_detail_query=Bill_detail.objects.filter(id=int(bill_detail_id[i]))
                if bill_detail_query.count()>0:       
                    bill_detail_obj=bill_detail_query[0]
                    (bill_detail,price_changed,detail_changed)=change_detail_price_product(bill_detail_obj,'DELETE',prev_bill_rcvr_org) # in updation WE DELETE first previous increased or decreased amount then again insert new
                    #now update the bill_detail_obj and product,product_detail same for opposit organization product,product_detail
                    bill_detail_obj.bill=bill_obj
                    bill_detail_obj.unit=unit_obj

                    bill_detail_obj.product=product_obj
                    bill_detail_obj.item_amount=item_amount[i]
                    bill_detail_obj.item_price=item_price[i]
                    bill_detail_obj.return_qty=return_qty[i]
                    bill_detail_obj.profit=0

                    try:        
                        bill_detail_obj.save() 
                        if bill_type=='SELLING':
                            purchased_price=product_obj.purchased_price
                            amount=(item_price[i]-purchased_price)*(item_amount[i]-return_qty[i])
                            ok=handle_profit_loss(bill_detail_obj,amount,operation='INCREASE')
                        
                        (bill_detail,price_changed,detail_changed)=change_detail_price_product(bill_detail_obj,'INSERT',bill_rcvr_org)    
                    except Exception as e:
                        ok=False
                        message=str(e)
                        (bill_detail,price_changed,detail_changed)=change_detail_price_product(bill_detail_obj,'DELETE',bill_rcvr_org)    
                        (bill_detail,price_changed,detail_changed)=change_detail_price_product(bill_detail_obj,'INSERT',prev_bill_rcvr_org) # in updation WE DELETE first previous increased or decreased amount then again insert new
                        print("e ",e)
    # print("bill_detail_query=",model_to_dict(bill_detail_obj))
    if ok==False:
        messages.error(request,message)
    else:  
        messages.success(request,message)
    return Response({"message":message,"ok":ok,"data":model_to_dict(bill_obj),"bill_id":bill_obj.id})    

@api_view(('GET',))
def search(request,bill_type,bill_no,bill_rcvr_org,creator,start_date,end_date):
    print("bill_type ",bill_type,"bill_no ",bill_no," bill_rcvr_org ",bill_rcvr_org," creator ",creator," start_date ",start_date," end_date ",end_date)
    start_date=re.sub('\t','',str(start_date))
    end_date=re.sub('\t','',str(end_date))
    
    try:
        start_date=datetime.strptime(start_date,"%Y-%m-%d")
    except Exception as e:
        if str(e)=="day is out of range for month":
            date_str=handle_day_out_of_range(start_date)
            start_date=datetime.strptime(date_str,'%Y-%m-%d')
        else:     
            return Response({"message":str(e),"ok":ok,"query":[],"statistics":[],"serializer_data":None})
    try:
        end_date=datetime.strptime(end_date,"%Y-%m-%d")
    except Exception as e:
        if str(e)=="day is out of range for month":
            date_str=handle_day_out_of_range(end_date)
            end_date=datetime.strptime(date_str,'%Y-%m-%d')
        else:     
            return Response({"message":str(e),"ok":ok,"query":[],"statistics":[],"serializer_data":None})
    
    self_organization,parent_organization=findOrganization(request)
    query=Bill.objects.filter(Q(date__range=[start_date,end_date]),Q(organization=parent_organization)|Q(bill_receiver__bill_rcvr_org=parent_organization))
    
    if int(bill_no)!=0:
        query=query.filter(bill_no=int(bill_no))
        print("########bill_no 2",query)
    if bill_type!=None and bill_type!="" and bill_type!="all":
        query=query.filter(
        bill_type__icontains=bill_type)
        print("#############bill_type 2",query)
        
    if bill_rcvr_org!=None and bill_rcvr_org!="" and bill_rcvr_org!="null" and bill_rcvr_org!="all":
        # query=query.filter(
        # rcvr_org__icontains=bill_rcvr_org)
        query=query.filter(Q(organization__id=int(bill_rcvr_org))|Q(bill_receiver__bill_rcvr_org__id=int(bill_rcvr_org)))
        
        # query=query.filter(Q(organization__name__icontains=bill_rcvr_org)|Q(bill_receiver__bill_rcvr_org__name__icontains=bill_rcvr_org))
        print("###########bill_rcvr_org 2",query)
    if creator!=None and creator!="" and creator!="null" and creator!="all":
        query=query.filter(
        creator__username__icontains=creator)
        print("#############creator 2",query)
    # if bill_type=="all":
    serializer=Bill_search_Serializer(query.order_by("-pk"),many=True)
    total_sum_purchase=query.filter(organization=parent_organization,
    bill_type='PURCHASE').aggregate(Sum("total"))['total__sum']
    payment_sum_purchase=query.filter(organization=parent_organization,
    bill_type='PURCHASE').aggregate(Sum("payment"))['payment__sum']
    

    total_sum_selling=query.filter(organization=parent_organization,
    bill_type='SELLING').aggregate(Sum("total"))['total__sum']
    payment_sum_selling=query.filter(organization=parent_organization,
    bill_type='SELLING').aggregate(Sum("payment"))['payment__sum']


    total_sum_payment=query.filter(organization=parent_organization,
    bill_type='PAYMENT').aggregate(Sum("total"))['total__sum']
    payment_sum_payment=query.filter(organization=parent_organization,
    bill_type='PAYMENT').aggregate(Sum("payment"))['payment__sum']

    total_sum_receivement=query.filter(organization=parent_organization,
    bill_type='RECEIVEMENT').aggregate(Sum("total"))['total__sum']
    receivement_sum=query.filter(organization=parent_organization,
    bill_type='RECEIVEMENT').aggregate(Sum("payment"))['payment__sum']
 
    total_sum_expense=query.filter(organization=parent_organization,
    bill_type='EXPENSE').aggregate(Sum("total"))['total__sum']
    payment_sum_expense=query.filter(organization=parent_organization,
    bill_type='EXPENSE').aggregate(Sum("payment"))['payment__sum']

    bill_count=query.count()
    if total_sum_purchase==None:
        total_sum_purchase=0
    if payment_sum_purchase==None:
        payment_sum_purchase=0
    
    if total_sum_selling==None:
        total_sum_selling=0
    if payment_sum_selling==None:
        payment_sum_selling=0

    if total_sum_payment==None:
        total_sum_payment=0
    if payment_sum_payment==None:
        payment_sum_payment=0
    
    if total_sum_expense==None:
        total_sum_expense=0
    if payment_sum_expense==None:
        payment_sum_expense=0
    
    
    if total_sum_receivement==None:
        total_sum_receivement=0
    if receivement_sum==None:
        receivement_sum=0 
    
    
    ################################################opposit##############################
    total_sum_purchase_from_bill_of_bill_rcvr_org=query.filter(bill_receiver__bill_rcvr_org=parent_organization,
    bill_type='SELLING').aggregate(Sum("total"))['total__sum']
    payment_sum_purchase_from_bill_of_bill_rcvr_org=query.filter(bill_receiver__bill_rcvr_org=parent_organization,
    bill_type='SELLING').aggregate(Sum("payment"))['payment__sum']
    

    total_sum_selling_from_bill_of_bill_rcvr_org=query.filter(bill_receiver__bill_rcvr_org=parent_organization,
    bill_type='PURCHASE').aggregate(Sum("total"))['total__sum']
    payment_sum_selling_from_bill_of_bill_rcvr_org=query.filter(bill_receiver__bill_rcvr_org=parent_organization,
    bill_type='PURCHASE').aggregate(Sum("payment"))['payment__sum']


    total_sum_payment_from_bill_of_bill_rcvr_org=query.filter(bill_receiver__bill_rcvr_org=parent_organization,
    bill_type='RECEIVEMENT').aggregate(Sum("total"))['total__sum']
    payment_sum_payment_from_bill_of_bill_rcvr_org=query.filter(bill_receiver__bill_rcvr_org=parent_organization,
    bill_type='RECEIVEMENT').aggregate(Sum("payment"))['payment__sum']

    total_sum_receivement_from_bill_of_bill_rcvr_org=query.filter(bill_receiver__bill_rcvr_org=parent_organization,
    bill_type='PAYMENT').aggregate(Sum("total"))['total__sum']
    receivement_sum_from_bill_of_bill_rcvr_org=query.filter(bill_receiver__bill_rcvr_org=parent_organization,
    bill_type='PAYMENT').aggregate(Sum("payment"))['payment__sum']
    

    bill_count=query.count()
    if total_sum_purchase_from_bill_of_bill_rcvr_org!=None:
        total_sum_purchase=total_sum_purchase+total_sum_purchase_from_bill_of_bill_rcvr_org
    if payment_sum_purchase_from_bill_of_bill_rcvr_org!=None:
        payment_sum_purchase=payment_sum_purchase+payment_sum_purchase_from_bill_of_bill_rcvr_org
    
    if total_sum_selling_from_bill_of_bill_rcvr_org!=None:
        total_sum_selling=total_sum_selling+total_sum_selling_from_bill_of_bill_rcvr_org

    if payment_sum_selling_from_bill_of_bill_rcvr_org!=None:
        payment_sum_selling=payment_sum_selling+payment_sum_selling_from_bill_of_bill_rcvr_org

    if total_sum_payment_from_bill_of_bill_rcvr_org!=None:  
        total_sum_payment=total_sum_payment+total_sum_payment_from_bill_of_bill_rcvr_org

    if payment_sum_payment_from_bill_of_bill_rcvr_org!=None:
        payment_sum_payment=payment_sum_payment+payment_sum_payment_from_bill_of_bill_rcvr_org

    if total_sum_receivement_from_bill_of_bill_rcvr_org!=None:
        total_sum_receivement=total_sum_receivement+total_sum_receivement_from_bill_of_bill_rcvr_org
    
    if receivement_sum_from_bill_of_bill_rcvr_org!=None:
        receivement_sum=receivement_sum+receivement_sum_from_bill_of_bill_rcvr_org
    #####################################summation of bill created by organization and by opposit organization#################
   
    baqaya_purchase=total_sum_purchase-payment_sum_purchase
    baqaya_selling=total_sum_selling-payment_sum_selling
    majmoa_upon_rcvr_org=total_sum_selling+payment_sum_payment+payment_sum_purchase
    majmoa_upon_shirkat=total_sum_purchase+payment_sum_selling+receivement_sum
    majmoa_baqaya=majmoa_upon_rcvr_org-majmoa_upon_shirkat
    # majmoa_upon_rcvr_org=query.aggregate(Sum("total"))['total__sum']
    # majmoa_upon_shirkat=query.aggregate(Sum("payment"))['payment__sum']
    possessed_cash_asset=(payment_sum_selling+receivement_sum)-(payment_sum_purchase+payment_sum_expense+payment_sum_payment)
    possessed_non_cash_asset=total_sum_purchase-total_sum_selling
    total_asset=possessed_cash_asset+possessed_non_cash_asset
    #current_profit=total_asset-initial_total_asset

    statistics=dict({
                    "majmoa_baqaya":majmoa_baqaya,
                    "majmoa_upon_rcvr_org":majmoa_upon_rcvr_org,
                    "majmoa_upon_shirkat":majmoa_upon_shirkat,
                    "bill_count":bill_count,
                    "total_sum_purchase":total_sum_purchase,
                    "payment_sum_purchase":payment_sum_purchase,
                    "baqaya_purchase":baqaya_purchase,
                    "total_sum_selling":total_sum_selling,
                    "payment_sum_selling":payment_sum_selling,
                    "baqaya_selling":baqaya_selling,
                    "total_sum_payment":total_sum_payment,
                    "payment_sum_payment":payment_sum_payment,
                    "total_sum_expense":total_sum_expense,
                    "payment_sum_expense":payment_sum_expense,
                    "total_sum_receivement":total_sum_receivement,
                    "payment_sum_receivement":receivement_sum,
                    "possessed_cash_asset":possessed_cash_asset,
                    "possessed_non_cash_asset":possessed_non_cash_asset,
                    "total_asset":total_asset,
                    # "current_profit":current_profit,
                    })      
    print("#####################################",query)
    query=query.order_by("-pk").values()
    return Response({"message":"OK","ok":True,"query":list(query),"statistics":statistics,"serializer_data":serializer.data})    