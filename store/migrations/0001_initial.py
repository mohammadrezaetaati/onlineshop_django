# Generated by Django 4.0.4 on 2022-05-19 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_time', models.DateTimeField(auto_now_add=True)),
                ('rate', models.PositiveSmallIntegerField()),
                ('text', models.TextField(blank=True, null=True)),
                ('image', models.ImageField(blank=True, null=True, upload_to='comments/')),
                ('like', models.PositiveIntegerField()),
                ('dislike', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='FavoriteProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='GeneralFeaturesCatalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('general_feature_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('average_rate', models.FloatField(default=0)),
                ('rate_votes_counter', models.PositiveIntegerField(default=0)),
                ('image', models.ImageField(default='default_product.png', upload_to='products/')),
            ],
        ),
        migrations.CreateModel(
            name='ProductGeneralFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gen_feature_value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='ProductSpecialFeature',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='SpecialFeaturesCatalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('special_feature_name', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='SpecialValuesCatalogue',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feature_value', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='SupplierProductDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price_per_unit', models.PositiveIntegerField(default=0)),
                ('available_quantity', models.PositiveIntegerField(default=0)),
                ('last_update_date_time', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='SupplierProductItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product')),
            ],
        ),
    ]
