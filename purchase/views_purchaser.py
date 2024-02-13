from django.shortcuts import render
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import PurchaserSerializer
from .models import Purchaser

@api_view(('GET','POST'))
def show(request,id="all"):
    print("id=",id)
    if id=="all":
        query_set=Purchaser.objects.all().order_by('-pk')
    else:
        query_set=Purchaser.objects.filter(id=int(id))

    serializer=PurchaserSerializer(query_set,many=True)

    return Response(serializer.data)

