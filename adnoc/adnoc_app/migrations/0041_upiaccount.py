# Generated by Django 4.2.3 on 2023-11-27 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0040_alter_adnocuser_refered_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='UPIAccount',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upiId', models.CharField(max_length=255)),
            ],
        ),
    ]