# Generated by Django 4.0.4 on 2022-06-14 18:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0003_alter_customer_options_alter_supplier_options_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='customerfavoritecategory',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='newslettersubscriber',
            old_name='customer_id',
            new_name='customer',
        ),
        migrations.RenameField(
            model_name='wallet',
            old_name='user_id',
            new_name='user',
        ),
    ]