from .models import Asset

possessed_asset=models.IntegerField(default=0)
loan_asset=models.IntegerField(default=0)
total_expected_asset=models.IntegerField(default=0)


def calculate_assets(bill_obj,purchase_detail_obj):
    total=bill_obj.total
    payment=bill_obj.payment
    bill_type=bill_obj.bill_type
    if bill_type=="PURCHASE":
        possessed_asset=possessed_asset-payment
        total_expected_asset=total_expected_asset-total
    elif bill_type=="PAYMENT":  
        possessed_asset=possessed_asset-payment
        total_expected_asset=total_expected_asset-payment
    
    elif bill_type=="SELLING":
        possessed_asset=possessed_asset+payment
        total_expected_asset=total_expected_asset+total
    elif bill_type=="RECEIVEMENT":
        possessed_asset=possessed_asset+payment
        total_expected_asset=total_expected_asset+total
    

    # bill_obj.store=store
    # bill_obj.vendor=vendor

