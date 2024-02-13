from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import *
from .models import *
import json
from common.organization import findOrganization
from django.http import HttpResponse
from django.template import loader 
from django.contrib.auth.decorators import login_required
from django.forms.models import model_to_dict

def change_bill_detail(operation,bill_type,product_detail,product_detail_of_bill_rcvr_org,net_amount,change_org,change_bill_rcvr_org):
    current_amount=product_detail.current_amount
    current_amount_bill_rcvr_org=product_detail_of_bill_rcvr_org.current_amount
    if operation=='INSERT':      
        if bill_type=="PURCHASE":
            current_amount=float(current_amount)+net_amount
            current_amount_bill_rcvr_org=float(current_amount_bill_rcvr_org)-net_amount
        elif bill_type=="SELLING":  
            current_amount=float(current_amount)-net_amount
            current_amount_bill_rcvr_org=float(current_amount_bill_rcvr_org)+net_amount
    else:
        if bill_type=="PURCHASE":
            current_amount=float(current_amount)-net_amount
            current_amount_bill_rcvr_org=float(current_amount_bill_rcvr_org)+net_amount
        elif bill_type=="SELLING":  
            current_amount=float(current_amount)+net_amount
            current_amount_bill_rcvr_org=float(current_amount_bill_rcvr_org)-net_amount
    try:
        if change_org:
            product_detail.current_amount=current_amount
        if change_bill_rcvr_org:
            product_detail_of_bill_rcvr_org.current_amount=current_amount_bill_rcvr_org
        product_detail.save()
        product_detail_of_bill_rcvr_org.save()
        changed=True
    except Exception as e:
        print("########change_price_product error",e)
        changed=False
        
    return (product_detail,product_detail_of_bill_rcvr_org,changed)

def change_prices(bill_type,item_price,product_price,product_price_of_bill_rcvr_org,change_org,change_bill_rcvr_org):
    if bill_type=="PURCHASE":
        if change_org:
            product_price.purchased_price=item_price
        if change_bill_rcvr_org:
            product_price_of_bill_rcvr_org.selling_price=item_price
    elif bill_type=="SELLING":
        if change_org:
            product_price.selling_price=item_price
        if change_bill_rcvr_org:
            product_price_of_bill_rcvr_org.purchased_price=item_price
    try:
        product_price.save()
        product_price_of_bill_rcvr_org.save()
        changed=True
    except Exception as e:
        print("product_price error ",e)
        changed=False
    return (product_price,product_price_of_bill_rcvr_org,changed)
    
# @login_required()
def change_detail_price_product(bill_detail,operation='INSERT',bill_rcvr_org=None,change_org=True,change_bill_rcvr_org=True):
    bill_type=bill_detail.bill.bill_type
    organization=bill_detail.bill.organization
    item_price=bill_detail.item_price
    item_amount=bill_detail.item_amount
    return_qty=bill_detail.return_qty
    product=bill_detail.product
    product_detail=product.product_detail      
    product_price=product.product_price  
    try:
        product_of_bill_rcvr_org=handle_product_for_bill_rcvr_org(product,bill_rcvr_org)
        print("###product_of_bill_rcvr_org",product_of_bill_rcvr_org)
        product_detail_of_bill_rcvr_org=product_of_bill_rcvr_org.product_detail
        product_price_of_bill_rcvr_org=product_of_bill_rcvr_org.product_price
    except Exception as e:
        print("########handle_product_for_bill_rcvr_org error",e)    
    ###########################change_price###################
    (product_price,product_price_of_bill_rcvr_org,price_changed)=change_prices(bill_type,item_price,product_price,product_price_of_bill_rcvr_org,change_org,change_bill_rcvr_org)    
      
    ###########################change_detail##################
    net_amount=(float(item_amount)-float(return_qty))
    (product_detail,product_detail_of_bill_rcvr_org,detail_changed)=change_bill_detail(operation,bill_type,product_detail,product_detail_of_bill_rcvr_org,net_amount,change_org,change_bill_rcvr_org)
    print(" price_changed,detail_changed ",price_changed,detail_changed)
    return (bill_detail,price_changed,detail_changed)  
# @login_required()
def create_product_price_detail_objs(product,data_price=None,data_detail=None):
    if data_price==None:
        data_price=dict()
        if hasattr(product,'product_price'):
            data_price['purchased_price']=product.product_price.purchased_price
            data_price['selling_price']=product.product_price.selling_price
        else:
            data_price['purchased_price']=0
            data_price['selling_price']=0
    if data_detail==None:
        data_detail=dict()
        data_detail['current_amount']=0
        data_detail['minimum_requirement']=1
    print("data_detail ",data_detail,"  data_price ",data_price," product ",product)
    product_price=None
    product_detail=None
    # product=Product.objects.get(id=product.id)s
    product_detail_query=Product_Detail.objects.filter(product=product)
    product_price_query=Product_Price.objects.filter(product=product)
    print("product_detail_query ",product_detail_query," product_price_query ",product_price_query)
    try:        
        if product_detail_query.count()>0:
            product_detail_query.update(**data_detail)
            product_detail=product_detail_query[0]
            print("product_detail_query.count()>0 ")
        else:
            print("product_detail_query.count()<0 ")
            product_detail=Product_Detail(product=product,**data_detail)
            product_detail.save()
        
        if product_price_query.count()>0:
            print("product_price_query.count()>0 ")
            product_price_query.update(**data_price)
            product_price=product_price_query[0]
        else:
            print("product_price_query.count()<=0 ")            
            product_price=Product_Price(product=product,**data_price)  
            product_price.save()
    except Exception as e:
        print('product detail and price Exception ',e)
    return (product_price,product_detail)


def handle_product_for_bill_rcvr_org(product_organization,organization):
    # this function make copy and create product from product_organization with the organization
    product_detail_data=model_to_dict(product_organization.product_detail)
    product_price_data=model_to_dict(product_organization.product_price)
    try:
        del product_detail_data['id']
    except Exception as e:
        print("del product_detail_data['id'] ",e)
    
    try:
        del product_price_data['id']
    except Exception as e:
        print("del product_price_data['id'] ",e)
    
    product_data=model_to_dict(product_organization)
    product_data['category']=Category.objects.get(id=int(product_data['category']))
    product_data['organization']=organization

    try:
        del product_data['id']
    except Exception as e: 
        print("del product_data['id'] e ",e)
    product_query=Product.objects.filter(item_name=product_data['item_name'],organization=organization)    
    print("product_data ",product_data)
    # product_data=model_to_dict(product_data)
    if product_query.count()>0:
        product=product_query[0]
    else:
        product=Product(**product_data)
    product.save()
    print("%%%%product ",product,"id ",product.id)
    try:
        query=Product_Detail.objects.filter(product=product)
        if query.count()>0:
            print("Product_Detail>0")
            query.update(**product_detail_data)
            product_detail=query[0]
        else:
            # print("Product_Detail=0")
            # print("$$$$$product ",model_to_dict(product))
            product_detail=Product_Detail()
            product_detail.product=product
            product_detail.descrip=product_detail_data['descrip']
            product_detail.minimum_requirement=1
            product_detail.current_amount=0
            
        query=Product_Price.objects.filter(product=product)
        if query.count()>0:
            print("Product_Price>0")
            query.update(**product_price_data)
            product_price=query[0]
        else:
            print("Product_Price>0")
            product_price=Product_Price() 
            product_price.product=product
        product_detail.save()
        print("product_detail.saved()")
        product_price.save()
        print("product_price.saved()")
    except Exception as e:
        print('product_price product_detail exception ',e)
    return product
        
def show_html(request,id=None):
    context={}
    (self_organization,parent_organization)=findOrganization(request)
    if id==None or id=="all":
        if request.user.is_superuser:
            query=Product.objects.all()
        else:
            query=Product.objects.filter(organization=parent_organization)
    else:
        query=Product.objects.filter(id=int(id))
    # print("product 4 ",dir(query[4].img))
    # print("query[0].img.url ",query[4].img.url)
    context['products']=query.order_by("-pk")
    context['products_length']=query.count()
    # context['']
    return render(request,'products/products.html',context)

@login_required(login_url='/admin')
def form(request,id=None):
    context={}
    if id==None:
        template=loader.get_template('products/product_form.html')
    else:
        context['product']=Product.objects.get(id=int(id))
        context['id']=int(id)
        template=loader.get_template('products/product_form.html')
    (self_organization,parent_organization)=findOrganization(request)
    # print("self_organization ",self_organization," parent_organization ",parent_organization)
    context['self_organization']=self_organization
    context['parent_organization']=parent_organization
    context['categories']=Category.objects.all()
    # HttpResponse("TES")
    # context['created_date']=date2jalali(datetime.now()) 
    return HttpResponse(template.render(context,request))
    # return render(request,'products/product_form.html',context)

@login_required(login_url='/admin')
@api_view(('PUT','POST'))
def create(request,id=None):
    data=request.data
    product=dict()
    product['id']=data['id']
    product['item_name']=data['item_name']
    product['category']=data['category']
    # product['organization']=data['organization']
    product['img']=request.FILES['img']
    # print("imagge",request.FILES['img'])
    product['is_active']=data['is_active']
    print(" data",data) 
    # return Response("test")
    product_detail=dict()
    product_detail['descrip']=data['descrip']
    if data['minimum_requirement']=='':
        data['minimum_requirement']=0
    product_detail['minimum_requirement']=data['minimum_requirement']
    if data['current_amount']=='':
        data['current_amount']=0
    product_detail['current_amount']=data['current_amount']
    
    product_price=dict()
    if data['purchased_price']=='':
        data['purchased_price']=0
    product_price['purchased_price']=data['purchased_price']
    if data['prev_purchased_price']=='':
        data['prev_purchased_price']=0
    product_price['previous_purchased_price']=data['prev_purchased_price']
    if data['selling_price']=='':
        data['selling_price']=0
    product_price['selling_price']=data['selling_price']
    if data['prev_selling_price']=='':
        data['prev_selling_price']=0
    product_price['previous_selling_price']=data['prev_selling_price']

    category_id=product['category']
    category=Category.objects.get(id=int(category_id))
    product['category']=category
    
    (self_organization,parent_organization)=findOrganization(request)
    product['organization']=self_organization
    # print('request.data ',type(product))
    # product=request.data
    # print('product ',product,' request data ',request.data,' product_detail ',product_detail)
    if 'is_active' in product.keys():
        if product['is_active']=='on':
            product['is_active']=True
        else:
            product['is_active']=False
    else:
        product['is_active']=False
    
    if product['id']=='' or product['id']==' ' or product['id']==None:
        product.pop('id')
    else:
        product['id']=int(product['id'])
    # print(" product_detail ",product_detail," product_price ",product_price," product ",product)
    product=Product(**product)
    print(' product ',product)
    try:
        product.save()
        data=product
        message='Product Inserted'
        ok=True
        print("EEEEEEEEEEEEEEEEE")
        (product_price,product_detail)=create_product_price_detail_objs(product,product_price,product_detail)
    except Exception as e:
        message=str(e)
        ok=False
        print('product execption ',e)
    # return HttpResponse("test")
    return Response({"message":message,"ok":ok,"id":data.id})
    # return HttpResponse(template.render(context,request))

@api_view(['GET'])
def show(request,organization_id="all",id="all"):
    print("id=",id," organization_id ",organization_id)
    if id=="all" or id=="" or id=='':
        if organization_id=="all":
            query_set=Product.objects.all().order_by('-pk')
        else:
            try:
                (self_organization,parent_organization)=findOrganization(request,organization_id)      
                # print("self_organization ",self_organization," parent_organization ",parent_organization)
                query_set=Product.objects.filter(organization=parent_organization).order_by('-pk')
                print("query_set ",query_set)
            except Exception as e:       
                query_set=Product.objects.filter(id=0).order_by('-pk')
    else:
        try:
            query_set=Product.objects.filter(id=int(id))
        except:
            query_set=Product.objects.filter(id=0).order_by('-pk')
    # print("query_set ",query_set)
    serializer=ProductSerializer(query_set,many=True)

    return Response(serializer.data)


@api_view(['GET'])
def select_service(request,html_id="all",dest=None):  
    print("########id=",html_id)
    if html_id=="all":
        query_set=Service.objects.all().order_by('-pk')
    else:
        language_obj=Languages.objects.get(language=dest)
        query_set=Service.objects.filter(html_id=str(html_id),dest=language_obj)
        
    print("select service=",query_set)
    serializer=ServiceSerializer(query_set,many=True)

    return Response(serializer.data)




