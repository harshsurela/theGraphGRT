# Generated by Django 4.2.3 on 2023-07-29 08:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0005_purchase_is_approved_purchase_purchase_date_wallet'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchase',
            name='is_approved',
            field=models.BooleanField(default=False, null=True),
        ),
    ]
