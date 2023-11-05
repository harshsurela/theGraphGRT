# Generated by Django 4.2.3 on 2023-07-30 11:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0004_purchase_is_approved_purchase_purchase_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='adnocuser',
            name='withdrawable_amount',
            field=models.FloatField(blank=True, default=0, null=True),
        ),
        migrations.CreateModel(
            name='WithdrawRequest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('request_date', models.DateTimeField()),
                ('acc_name', models.CharField(max_length=60)),
                ('acc_no', models.CharField(max_length=20)),
                ('ifsc', models.CharField(max_length=20)),
                ('mobile_number', models.CharField(max_length=15)),
                ('status', models.CharField(default='Pending', max_length=10)),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]