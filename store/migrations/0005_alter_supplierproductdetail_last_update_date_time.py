# Generated by Django 4.0.4 on 2022-05-30 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0004_supplierproductitem_unique product for supplier'),
    ]

    operations = [
        migrations.AlterField(
            model_name='supplierproductdetail',
            name='last_update_date_time',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
