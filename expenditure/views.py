from django.shortcuts import render
from jalali_date import date2jalali
from datetime import datetime
from common.organization import findOrganization
from purchase.forms import Bill_Form
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.http import HttpResponse
from rest_framework.decorators import api_view
from purchase.views_bill import getBillNo
from configuration.models import Organization
from purchase.models import Bill
from django.forms.models import model_to_dict
from rest_framework.response import Response
# Create your views here.
@login_required(login_url='/admin')
def expense_form(request,id=None):
    template=loader.get_template('bill/expenditure/expense_form.html')
    date = date2jalali(datetime.now())
    year=date.strftime('%Y')
    self_organization,parent_organization=findOrganization(request)
    form=Bill_Form()
    context={}
    form.fields['date'].initial=date
    bill_no=getBillNo(request,parent_organization.id,parent_organization.id,"EXPENSE")
    context={
        'form':form,
        'bill_no':bill_no,
        'organization':parent_organization,
        'date':date,
    } 
    if id!=None:
        bill=Bill.objects.filter(id=int(id))
        context['bill']=bill
    return HttpResponse(template.render(context,request))


@login_required(login_url='/admin')
@api_view(['POST','PUT'])
def expense_insert(request):  
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
    ############before request.data  and request.data.getlist
    

    organization=request.data.get("organization")
    organization=Organization.objects.get(id=int(organization))
    (self_organization,parent_organization)=findOrganization(request)

    bill_type=request.data.get("bill_type",None)
    creator=request.user
    total=request.data.get("total",0)
    if total=='' or total=="" or total==None:
        total=0
    payment=request.data.get("total_payment",0)      
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
    
        previous_bill_type =bill_obj.bill_type
        bill_obj.total=total
        bill_obj.payment=payment
        bill_obj.bill_type=bill_type
   
    else: ############### new insert Bill if not in system#############
        opposit_bill='EXPENSE'
        bill_query=Bill.objects.filter(bill_no=int(bill_no),year=int(year),bill_type=bill_type,organization=organization)
        if bill_query.count()>0: # if we are not having update then we check if such bill present or not if exists we not enter
            ok=False
            message="The Bill is already in system search for Bill No {} Bill Type {} Year {} ".format(bill_no,bill_type,year)
            return Response({"message":message,"ok":ok})
        bill_obj=Bill(bill_type=bill_type,date=date,year=year,bill_no=bill_no,organization=organization,creator=creator,total=total,payment=payment)
    try:
        bill_obj.save()
        ok=True
        message="bill No {} Successfully Insert".format(bill_no)
    except Exception as e:
        ok=False
        message=str(e)
        print("e ",e)
        return Response({"message":message,"ok":ok})
    ######################## if item_name total_amount is < payment and payment is more then reject ############ 
    return Response({"message":message,"ok":ok,"data":model_to_dict(bill_obj),"bill_id":bill_obj.id})    
