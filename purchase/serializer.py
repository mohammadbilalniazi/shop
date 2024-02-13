from rest_framework import serializers
from .models import Bill_detail,Bill,Purchaser,Bill_Description,Bill_Receiver
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields="__all__"

class Bill_detail_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Bill_detail
        fields='__all__'
        fields=["id","product","item_amount","item_price","return_qty","profit"]



       
class Bill_Description_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Bill_Description
        fields='__all__'

class Bill_Receiver_Serializer(serializers.ModelSerializer):
    class Meta:
        model=Bill_Receiver
        fields='__all__'


class Bill_search_Serializer(serializers.ModelSerializer):
    # bill_description=Bill_Description_Serializer()
    bill_receiver=Bill_Receiver_Serializer()
    class Meta:
        model=Bill  
        fields=["id","bill_receiver","bill_type","bill_no","payment","date","organization","creator","total"] #month===> kaifyath_haziri

class Bill_Create_Serializer(serializers.ModelSerializer):
    bill_detail_set = Bill_detail_Serializer(many=True)
    bill_receiver=Bill_Receiver_Serializer()
    bill_description=Bill_Description_Serializer()
    class Meta:
        model=Bill
        # fields=["id","bill_detail_set","bill_description","payment","date","creator","total"] #month===> kaifyath_haziri
        fields=["id","bill_receiver","payment","date","creator","total"] #month===> kaifyath_haziri

    def create(self, validated_data):
        bill_detail_set = validated_data.pop('bill_detail_set')
        bill_description = validated_data.pop('bill_description')
        bill = Bill.objects.create(**validated_data)
        bill.save()
        for bill_detail in bill_detail_set:
            bill_detail_obj = Bill_detail.objects.create(bill=bill, **bill_detail)
            bill_detail_obj.save()
        bill_description_obj=Bill_Description.objects.create(bill=bill,**bill_description)
        bill_description_obj.save()
        return bill
