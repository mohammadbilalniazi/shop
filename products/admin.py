from django.contrib import admin
from .models import Product,Category,Vendors,Service,SubService,Store,Unit,Product_Price
from pathlib import PurePath
from common.organization import findOrganization
# from django.conf import settings
from django.utils.html import format_html
# Register your models here.


@admin.register(Store) 
class StoreAdmin(admin.ModelAdmin):
    list_display=("name","location","is_active")

@admin.register(Product_Price)
class ProductPriceAdmin(admin.ModelAdmin):
    list_display=("product","purchased_price","selling_price","previous_selling_price")




@admin.register(Unit) 
class UnitAdmin(admin.ModelAdmin):
    list_display=("name","description","is_active")


@admin.register(Category) 
class CategoryAdmin(admin.ModelAdmin):
    list_display=("name","description","is_active","image_tag")
    readonly_fields = ['image_tag']
    

@admin.register(Product) 
class ProductAdmin(admin.ModelAdmin):
    # list_display=("organization","item_name","get_detail","category","get_minimum_requirement","get_item_amount_available","get_row","get_column","get_purchased_price","get_selling_price","image_tag")
    list_display=("organization","item_name","get_detail","category","get_minimum_requirement","get_item_amount_available","get_row","get_column","get_purchased_price","get_selling_price")
    list_filter=("category","item_name")
    # fields = ['image_tag']
    # readonly_fields = ['image_tag']
    def queryset(self, request):
        qs = super(Product, self).queryset(request)
        organization=findOrganization(request)
        print("organization ",organization)
        # if request.user.is_superuser:
        #     return qs
        return qs.filter(organization=organization)

    def get_column(self, obj):
        if obj.row_column_address:
            return obj.row_column_address.column
        else:
            return None

    def get_row(self, obj):
        if obj.row_column_address:
            return obj.row_column_address.row
        else:
            return None

    def get_detail(self, obj):
        if obj.product_detail:
            return obj.product_detail.description
        else:
            return obj.product_detail

 
    def get_minimum_requirement(self, obj):
        if obj.product_detail:
            return obj.product_detail.minimum_requirement
        else:
            return obj.product_detail
            
    def get_item_amount_available(self, obj):
        if obj.product_detail:
            return obj.product_detail.current_amount
        else:
            return obj.product_detail
    
    def get_purchased_price(self, obj):
        if obj.product_price:
            return obj.product_price.purchased_price
        else:
            return obj.product_price

    def get_selling_price(self, obj):
        if obj.product_price:
            return obj.product_price.selling_price
        else:
            return obj.product_price

# @admin.register(Vendors) 
# class VendorAdmin(admin.ModelAdmin):
#     list_display=("name","description","is_active")

 
# @admin.register(Service) 
# class ServiceAdmin(admin.ModelAdmin):
#     list_display=("name","category","dest","detail","html_id","is_active")

 
# @admin.register(SubService) 
# class SubSerivceAdmin(admin.ModelAdmin):
#     list_display=("service","sub_service_name","dest","detail","html_id","is_active")


    

    # Service=("service","uploader","file","is_active") 