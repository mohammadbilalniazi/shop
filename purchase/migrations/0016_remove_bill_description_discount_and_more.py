# Generated by Django 4.1.1 on 2023-10-06 07:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0015_bill_receiver_store_alter_bill_year'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill_description',
            name='discount',
        ),
        migrations.AlterField(
            model_name='bill_description',
            name='status',
            field=models.SmallIntegerField(choices=[(0, 'CANCELLED'), (1, 'CREATED')], default=0),
        ),
    ]