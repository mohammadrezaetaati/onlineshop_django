# Generated by Django 4.0.4 on 2022-05-19 13:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('store', '0001_initial'),
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='supplierproductitem',
            name='supplier',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.supplier'),
        ),
        migrations.AddField(
            model_name='supplierproductdetail',
            name='sup_pr_item_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.supplierproductitem'),
        ),
        migrations.AddField(
            model_name='specialvaluescatalogue',
            name='feature_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.specialfeaturescatalogue'),
        ),
        migrations.AddField(
            model_name='productspecialfeature',
            name='spe_feature_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.specialfeaturescatalogue'),
        ),
        migrations.AddField(
            model_name='productspecialfeature',
            name='spe_feature_value',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.specialvaluescatalogue'),
        ),
        migrations.AddField(
            model_name='productspecialfeature',
            name='sup_pr_detail_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.supplierproductdetail'),
        ),
        migrations.AddField(
            model_name='productgeneralfeature',
            name='gen_feature_key',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='store.generalfeaturescatalogue'),
        ),
        migrations.AddField(
            model_name='productgeneralfeature',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.AddField(
            model_name='product',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='store.category'),
        ),
        migrations.AddField(
            model_name='product',
            name='suppliers',
            field=models.ManyToManyField(through='store.SupplierProductItem', to='user.supplier'),
        ),
        migrations.AddField(
            model_name='favoriteproduct',
            name='favorite_category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.customerfavoritecategory'),
        ),
        migrations.AddField(
            model_name='favoriteproduct',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.AddField(
            model_name='comment',
            name='customer_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='user.customer'),
        ),
        migrations.AddField(
            model_name='comment',
            name='product_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='store.product'),
        ),
        migrations.AddField(
            model_name='category',
            name='general_features',
            field=models.ManyToManyField(to='store.generalfeaturescatalogue'),
        ),
        migrations.AddField(
            model_name='category',
            name='parent_category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.RESTRICT, to='store.category'),
        ),
        migrations.AddField(
            model_name='category',
            name='special_features',
            field=models.ManyToManyField(to='store.specialfeaturescatalogue'),
        ),
        migrations.AddConstraint(
            model_name='productspecialfeature',
            constraint=models.UniqueConstraint(fields=('sup_pr_detail_id', 'spe_feature_key'), name='unique special feature'),
        ),
        migrations.AddConstraint(
            model_name='productgeneralfeature',
            constraint=models.UniqueConstraint(fields=('product_id', 'gen_feature_key'), name='unique general feature'),
        ),
    ]