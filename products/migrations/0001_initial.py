# Generated by Django 4.1.1 on 2023-03-30 04:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import products.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('configuration', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('description', models.TextField(blank=True, max_length=100, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to=products.models.Category_directory_path)),
                ('is_active', models.BooleanField(default=True)),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='products.category')),
            ],
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('detail', models.TextField(blank=True, null=True)),
                ('html_id', models.CharField(max_length=50)),
                ('img', models.ImageField(blank=True, null=True, upload_to=products.models.user_directory_path, validators=[products.models.validate_image])),
                ('is_active', models.BooleanField(default=None, null=True)),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='products.category')),
                ('dest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='configuration.languages')),
                ('organization', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='configuration.organization')),
            ],
            options={
                'unique_together': {('name', 'organization')},
            },
        ),
        migrations.CreateModel(
            name='SubService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_service_name', models.CharField(max_length=50, null=True)),
                ('detail', models.TextField(blank=True, null=True)),
                ('html_id', models.CharField(max_length=50, unique=True)),
                ('is_active', models.BooleanField(default=None, null=True)),
                ('dest', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='configuration.languages')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.service')),
            ],
            options={
                'unique_together': {('sub_service_name', 'service', 'dest')},
            },
        ),
        migrations.CreateModel(
            name='Unit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Vendors',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True)),
                ('account', models.CharField(blank=True, max_length=30, null=True)),
                ('description', models.CharField(blank=True, max_length=100, null=True)),
                ('is_active', models.BooleanField(default=True)),
                ('user', models.OneToOneField(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='SubService_Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(unique=True, upload_to='uploads/%Y-%m-%d')),
                ('is_active', models.BooleanField(default=None, null=True)),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.subservice')),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Service_Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(unique=True, upload_to='uploads/%Y-%m-%d')),
                ('is_active', models.BooleanField(default=None, null=True)),
                ('service', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='products.service')),
                ('uploader', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Store',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20, unique=True)),
                ('is_active', models.BooleanField(default=True)),
                ('admin', models.CharField(blank=True, max_length=100, null=True)),
                ('location', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='configuration.location')),
            ],
            options={
                'unique_together': {('name', 'location')},
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=50)),
                ('detail', models.CharField(blank=True, max_length=200, null=True)),
                ('minimum_requirement', models.IntegerField()),
                ('item_amount_available', models.IntegerField()),
                ('row', models.IntegerField(blank=True, null=True)),
                ('column', models.IntegerField(blank=True, null=True)),
                ('purchased_price', models.IntegerField(default=None, null=True)),
                ('selling_price', models.IntegerField(default=None, null=True)),
                ('img', models.ImageField(blank=True, null=True, upload_to='Products', validators=[products.models.validate_image])),
                ('category', models.ForeignKey(default=None, on_delete=django.db.models.deletion.DO_NOTHING, to='products.category')),
                ('organization', models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='configuration.organization')),
            ],
            options={
                'unique_together': {('item_name', 'category', 'organization'), ('item_name', 'organization')},
            },
        ),
    ]
