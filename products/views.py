from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import ProductSerializer,VendorSerializer
from .models import Product,Vendors

@api_view(('GET','POST'))
def show(request,id=None):
    print("id=",id)
    if id==None:
        query_set=Product.objects.all().order_by('-pk')
    else:
        query_set=Product.objects.filter(id=int(id))

    serializer=ProductSerializer(query_set,many=True)

    return Response(serializer.data)


@api_view(('GET','POST'))
def show(request,id=None,name=None):
    print("id=",id)
    if id==None:
        query_set=Vendors.objects.all().order_by('-pk')
        if name!=None and name!="":
            query_set.filter(name__icontains=name)
    else:
        query_set=Vendors.objects.filter(id=int(id))

    serializer=VendorSerializer(query_set,many=True)

    return Response(serializer.data)


