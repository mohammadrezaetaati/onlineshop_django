# Generated by Django 4.0.4 on 2022-06-10 10:50

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0006_product_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='rate',
            field=models.PositiveSmallIntegerField(default=3, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
