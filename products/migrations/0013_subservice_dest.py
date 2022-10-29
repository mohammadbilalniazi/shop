# Generated by Django 4.1.1 on 2022-10-21 18:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0009_alter_language_detail_unique_together'),
        ('products', '0012_service_dest'),
    ]

    operations = [
        migrations.AddField(
            model_name='subservice',
            name='dest',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='configuration.languages'),
        ),
    ]