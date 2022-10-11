# Generated by Django 4.1.1 on 2022-10-08 14:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('products', '0004_serivce_subserivce'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subserivce',
            old_name='service_id',
            new_name='html_id',
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('service_name', models.CharField(max_length=50, unique=True)),
                ('detail', models.TextField(blank=True, null=True)),
                ('html_id', models.CharField(max_length=50, unique=True)),
                ('service_incharger', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=None, null=True)),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='products.category')),
            ],
        ),
        migrations.AlterField(
            model_name='subserivce',
            name='sub_service_name',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.service'),
        ),
        migrations.DeleteModel(
            name='Serivce',
        ),
    ]