# Generated by Django 4.2.3 on 2023-08-01 21:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0020_userrecharge_is_credited_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userrecharge',
            name='user_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='userPro', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='transactions',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('trans_date', models.DateTimeField()),
                ('credited', models.BooleanField()),
                ('tag', models.TextField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
