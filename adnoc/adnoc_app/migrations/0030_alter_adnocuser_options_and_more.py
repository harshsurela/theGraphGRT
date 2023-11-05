# Generated by Django 4.2.3 on 2023-08-03 10:32

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0029_alter_adnocuser_referal_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adnocuser',
            options={'verbose_name': 'user', 'verbose_name_plural': 'users'},
        ),
        migrations.AlterUniqueTogether(
            name='adnocuser',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='adnocuser',
            name='mobile_number',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterField(
            model_name='adnocuser',
            name='referal_code',
            field=models.TextField(default=uuid.UUID('c1fa046d-a887-49d1-81eb-f6fcf1d8c7db')),
        ),
        migrations.AlterField(
            model_name='adnocuser',
            name='username',
            field=models.CharField(max_length=100),
        ),
    ]