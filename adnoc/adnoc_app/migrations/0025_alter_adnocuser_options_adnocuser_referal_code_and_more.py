# Generated by Django 4.2.3 on 2023-08-03 09:35

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0024_merge_20230802_1807'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='adnocuser',
            options={},
        ),
        migrations.AddField(
            model_name='adnocuser',
            name='referal_code',
            field=models.TextField(default=uuid.UUID('b756ec3b-d136-426e-8115-37a27d4c1484')),
        ),
        migrations.AddField(
            model_name='adnocuser',
            name='refered_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='adnocuser',
            name='mobile_number',
            field=models.CharField(max_length=15, unique=True),
        ),
        migrations.AlterUniqueTogether(
            name='adnocuser',
            unique_together={('username', 'mobile_number')},
        ),
    ]
