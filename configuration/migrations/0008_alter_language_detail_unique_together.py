# Generated by Django 4.1.1 on 2022-10-21 13:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('configuration', '0007_alter_language_detail_unique_together_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='language_detail',
            unique_together={('id_field', 'src', 'dest')},
        ),
    ]