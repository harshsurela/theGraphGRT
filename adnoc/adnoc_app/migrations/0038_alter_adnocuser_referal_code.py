# Generated by Django 4.2.3 on 2023-08-04 12:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0037_alter_adnocuser_referal_code'),
    ]

    operations = [
        migrations.AlterField(
            model_name='adnocuser',
            name='referal_code',
            field=models.TextField(default=uuid.UUID('05f6375f-ac14-46ba-9e62-a4e1ddb69360')),
        ),
    ]
