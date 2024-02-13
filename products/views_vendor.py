from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import VendorSerializer
from .models import Product,Vendors

@api_view(('GET','DELETE'))
def vendors_show(request,id="all"):
    print("vendors_show id=",id)
    # if request.type=="DELETE":
    if id=="all":
        query_set=Vendors.objects.all().order_by('-pk')
    else:
        query_set=Vendors.objects.filter(name=str(id))

    serializer=VendorSerializer(query_set,many=True)
    # print("serialzier ",serializer)
    return Response(serializer.data)



@api_view(['POST'])
def post(request,id=None):
    # print("id=",id)
    data=request.data
    if id==None:
        query_set=Vendors.objects.all().order_by('-pk')
    else:
        query_set=Vendors.objects.filter(id=int(id))

    serializer=VendorSerializer(query_set,many=True)
    # print("serialzier ",serializer)
    return Response(serializer.data)




