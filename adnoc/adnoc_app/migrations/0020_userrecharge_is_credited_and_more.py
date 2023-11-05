# Generated by Django 4.2.3 on 2023-08-01 20:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0019_rename_recharge_userrecharge'),
    ]

    operations = [
        migrations.AddField(
            model_name='userrecharge',
            name='is_credited',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='userrecharge',
            name='recharge_amount',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
