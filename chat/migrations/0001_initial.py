# Generated by Django 4.1.1 on 2023-03-27 03:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
                ('creator', models.CharField(blank=True, default=None, max_length=25, null=True)),
                ('date_time', models.DateTimeField(blank=True, null=True)),
                ('status', models.SmallIntegerField(choices=[(1, 'OPEN'), (2, 'CLOSED'), (3, 'CANCELED'), (4, 'SUSPENDED')], default=1)),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.CharField(max_length=1000)),
                ('date', models.DateTimeField(blank=True)),
                ('user', models.CharField(max_length=100)),
                ('replied_to', models.IntegerField(blank=True, default=None, null=True)),
                ('room', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='chat.room')),
            ],
        ),
    ]
