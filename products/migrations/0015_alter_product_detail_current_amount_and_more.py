# Generated by Django 4.1.1 on 2023-11-16 21:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0014_alter_product_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product_detail',
            name='current_amount',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=22),
        ),
        migrations.AlterField(
            model_name='product_price',
            name='previous_purchased_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=22, null=True),
        ),
        migrations.AlterField(
            model_name='product_price',
            name='previous_selling_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=22, null=True),
        ),
        migrations.AlterField(
            model_name='product_price',
            name='purchased_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=22, null=True),
        ),
        migrations.AlterField(
            model_name='product_price',
            name='selling_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=22, null=True),
        ),
    ]
