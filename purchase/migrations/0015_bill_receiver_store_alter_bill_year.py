# Generated by Django 4.1.1 on 2023-06-16 01:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0010_alter_product_is_active'),
        ('purchase', '0014_alter_bill_receiver_approval_user'),
    ]

    operations = [
        migrations.AddField(
            model_name='bill_receiver',
            name='store',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='products.store', to_field='name'),
        ),
        migrations.AlterField(
            model_name='bill',
            name='year',
            field=models.SmallIntegerField(default=1401),
        ),
    ]
