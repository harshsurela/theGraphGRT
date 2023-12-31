# Generated by Django 4.2.3 on 2023-07-27 18:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('adnoc_app', '0003_rename_products_product'),
    ]

    operations = [
        migrations.AddField(
            model_name='purchase',
            name='transaction_id',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='purchase',
            name='transaction_image',
            field=models.ImageField(null=True, upload_to='transaction'),
        ),
        migrations.AlterField(
            model_name='product',
            name='prod_img',
            field=models.ImageField(upload_to='products'),
        ),
    ]
