# Generated by Django 4.1.1 on 2023-05-18 09:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0012_alter_bill_description_bill'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill_receiver',
            name='approval_date',
            field=models.DateField(blank=True, default='', null=True),
        ),
    ]