# Generated by Django 4.1.1 on 2024-02-12 15:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('purchase', '0016_remove_bill_description_discount_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bill_detail',
            name='profit',
        ),
        migrations.AddField(
            model_name='bill',
            name='profit',
            field=models.IntegerField(default=None, null=True),
        ),
    ]