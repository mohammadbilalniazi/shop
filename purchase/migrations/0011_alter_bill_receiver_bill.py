# Generated by Django 4.1.1 on 2023-04-30 10:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0010_remove_bill_rcvr_org_remove_bill_rcvr_org_aprv_usr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill_receiver',
            name='bill',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='purchase.bill'),
        ),
    ]