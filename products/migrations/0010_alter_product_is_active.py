# Generated by Django 4.1.1 on 2023-04-30 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0009_rename_item_amount_available_product_detail_crnt_amt_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='is_active',
            field=models.BooleanField(default=True, null=True),
        ),
    ]
