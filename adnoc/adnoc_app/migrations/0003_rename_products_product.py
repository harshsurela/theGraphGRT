# Generated by Django 4.2.3 on 2023-07-27 14:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0002_products_purchase'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Products',
            new_name='Product',
        ),
    ]