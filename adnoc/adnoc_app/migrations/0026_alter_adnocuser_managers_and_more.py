# Generated by Django 4.2.3 on 2023-08-03 09:53

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0025_alter_adnocuser_options_adnocuser_referal_code_and_more'),
    ]

    operations = [
        migrations.AlterModelManagers(
            name='adnocuser',
            managers=[
            ],
        ),
        migrations.AlterField(
            model_name='adnocuser',
            name='referal_code',
            field=models.TextField(default=uuid.UUID('57aea631-93e8-4b20-801f-20d7f2879135')),
        ),
    ]
