# Generated by Django 4.2.3 on 2023-08-03 09:59

import django.contrib.auth.models
from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0027_alter_adnocuser_mobile_number_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='adnocuser',
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='adnocuser',
            name='referal_code',
            field=models.TextField(default=uuid.UUID('f05de1a3-ef09-4db9-9e05-adeb9251f257')),
        ),
    ]
