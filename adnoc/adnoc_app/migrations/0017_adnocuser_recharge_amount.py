# Generated by Django 4.2.3 on 2023-08-01 17:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0016_alter_adnocuser_mobile_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='adnocuser',
            name='recharge_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
    ]
