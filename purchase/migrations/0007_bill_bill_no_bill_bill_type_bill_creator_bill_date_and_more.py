# Generated by Django 4.1.1 on 2023-04-08 16:50

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0003_rename_username_member_user_user'),
        ('products', '0002_alter_store_unique_together_store_organization_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchase', '0006_rename_bill_transactions_bill_transaction'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill',
            name='bill_no',
            field=models.IntegerField(default=None),
        ),
        migrations.AddField(
            model_name='bill',
            name='bill_type',
            field=models.CharField(default='PURCHASE', max_length=9),
        ),
        migrations.AddField(
            model_name='bill',
            name='creator',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
        migrations.AddField(
            model_name='bill',
            name='date',
            field=models.DateField(null=True),
        ),
        migrations.AddField(
            model_name='bill',
            name='organization',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='configuration.organization', to_field='name'),
        ),
        migrations.AddField(
            model_name='bill',
            name='payment',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='bill',
            name='total',
            field=models.DecimalField(decimal_places=5, default=0.0, max_digits=20),
        ),
        migrations.AddField(
            model_name='bill',
            name='year',
            field=models.IntegerField(default=1401),
        ),
        migrations.AlterField(
            model_name='bill',
            name='bill_rcvr_org',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterField(
            model_name='bill',
            name='rcvr_org_aprv_usr',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
        migrations.AlterUniqueTogether(
            name='bill',
            unique_together={('organization', 'year', 'bill_no', 'bill_type')},
        ),
        migrations.CreateModel(
            name='Bill_Description',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.SmallIntegerField(choices=[(0, 'CANCELLED'), (1, 'CREATED')], default=1)),
                ('discount', models.IntegerField(default=0)),
                ('currency', models.CharField(default='afg', max_length=7)),
                ('bill', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='purchase.bill')),
                ('shipment_location', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='configuration.location', to_field='city')),
                ('store', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.store', to_field='name')),
            ],
        ),
        migrations.RemoveField(
            model_name='bill',
            name='currency',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='discount',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='shipment_location',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='status',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='store',
        ),
        migrations.RemoveField(
            model_name='bill',
            name='vendor',
        ),
        migrations.DeleteModel(
            name='Bill_Transaction',
        ),
    ]