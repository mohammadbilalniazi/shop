# Generated by Django 4.1.1 on 2023-05-18 09:03

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('purchase', '0013_alter_bill_receiver_approval_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bill_receiver',
            name='approval_user',
            field=models.ForeignKey(blank=True, default='', null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL, to_field='username'),
        ),
    ]
