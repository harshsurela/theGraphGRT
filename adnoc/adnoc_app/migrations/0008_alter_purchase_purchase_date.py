# Generated by Django 4.2.3 on 2023-07-29 10:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0007_wallethistory_delete_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='purchase_date',
            field=models.DateTimeField(null=True),
        ),
    ]
