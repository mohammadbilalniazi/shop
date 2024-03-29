# Generated by Django 4.1.1 on 2023-04-10 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0005_remove_product_detail_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Product_Detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('detail', models.TextField(blank=True, null=True)),
                ('minimum_requirement', models.IntegerField()),
                ('item_amount_available', models.IntegerField()),
                ('product', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.product', unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='product_price_detial',
            name='product',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.product', unique=True),
        ),
        migrations.DeleteModel(
            name='Product_Detial',
        ),
    ]
