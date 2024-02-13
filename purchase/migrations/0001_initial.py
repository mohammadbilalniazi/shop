# Generated by Django 4.1.1 on 2023-03-30 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('configuration', '0001_initial'),
        ('products', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bill_type', models.CharField(default='PURCHASE', max_length=9)),
                ('date', models.DateField()),
                ('year', models.IntegerField(default=1401)),
                ('status', models.SmallIntegerField(choices=[(0, 'CANCELLED'), (1, 'CREATED')], default=1)),
                ('bill_no', models.IntegerField(default=None)),
                ('discount', models.IntegerField(default=0)),
                ('total', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('payment', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('currency', models.CharField(default='afg', max_length=7)),
                ('creator', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, to_field='username')),
                ('organization', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='configuration.organization')),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.store', to_field='name')),
                ('vendor', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.vendors', to_field='name')),
            ],
            options={
                'unique_together': {('organization', 'year', 'bill_no')},
            },
        ),
        migrations.CreateModel(
            name='Purchaser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('account', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Bill_detail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_amount', models.IntegerField()),
                ('item_price', models.DecimalField(decimal_places=5, default=0.0, max_digits=15)),
                ('return_qty', models.IntegerField(blank=True, null=True)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.bill')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='products.product')),
                ('unit', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.unit')),
            ],
            options={
                'verbose_name_plural': 'Bill detail',
                'unique_together': {('bill', 'product')},
            },
        ),
    ]
