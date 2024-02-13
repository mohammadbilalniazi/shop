from rest_framework import serializers
from .models import Product,Product_Price ,Vendors ,Service , SubService,Unit,Store

class ProductPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product_Price
        fields="__all__"

class ProductSerializer(serializers.ModelSerializer): #serializers.ModelSerializer
    product_price=ProductPriceSerializer()

    class Meta:
        model = Product
        fields =['id','item_name','organization','product_price']

class VendorSerializer(serializers.ModelSerializer):
    class Meta:
        model=Vendors
        fields="__all__"


class SubServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model=SubService
        fields=["service","sub_service_name","detail","html_id","is_active"]



class UnitSerializer(serializers.ModelSerializer):
    class Meta:
        model=Unit
        fields="__all__"
        
class StoreSerializer(serializers.ModelSerializer):
    class Meta:
        model=Store
        fields="__all__"
# SubService=("service","detail","html_id","is_active")
# Service=("service_name","category","detail","html_id","service_incharger","is_active")
#     
class ServiceSerializer(serializers.ModelSerializer):
    subservice_set=SubServiceSerializer(many=True)
    class Meta:
        model=Service
        fields=["subservice_set","service_name","category","detail","html_id","service_incharger","is_active"]
