# Generated by Django 4.2.3 on 2023-07-29 10:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0008_alter_purchase_purchase_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='wallethistory',
            name='transaction_date',
            field=models.DateTimeField(),
        ),
    ]
