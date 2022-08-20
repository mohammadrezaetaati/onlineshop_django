from django.db import models
from django.utils.text import slugify
from django.core.validators import MaxValueValidator, MinValueValidator 

from user.models import Customer, Supplier, CustomerFavoriteCategory


class Category(models.Model):
    name = models.CharField(max_length= 100)
    parent_category = models.ForeignKey('Category', on_delete= models.RESTRICT, null= True, blank= True)
    general_features = models.ManyToManyField('GeneralFeaturesCatalogue')
    special_features = models.ManyToManyField('SpecialFeaturesCatalogue')

    def __str__(self) -> str:
        if self.parent_category:
            return f"{self.parent_category} / {self.name}"
        return self.name


class Product(models.Model):
    name = models.CharField(max_length= 255)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete= models.RESTRICT)
    average_rate = models.FloatField(default=0)
    rate_votes_counter = models.PositiveIntegerField(default= 0)
    suppliers = models.ManyToManyField(Supplier, through= 'SupplierProductItem')
    image = models.ImageField(upload_to= 'products/', default= 'default_product.png')
    slug = models.SlugField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name

    def save(self, *args, **kwargs):
        if self.slug is None:
            self.slug = slugify(self.name, allow_unicode=True)
        return super().save(*args, **kwargs)

    def rate_calculator(self):
        rate = self.comment_set.aggregate(average=models.Avg('rate'), count=models.Count('rate'))
        self.average_rate = '{:0.1f}'.format(rate['average'])
        self.rate_votes_counter = rate['count']
        return self.save()


class FavoriteProduct(models.Model):
    favorite_category_id = models.ForeignKey(CustomerFavoriteCategory, on_delete=models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete=models.CASCADE)


class Comment(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete= models.CASCADE)
    product_id = models.ForeignKey(Product, on_delete= models.CASCADE)
    date_time = models.DateTimeField(auto_now_add= True)
    rate = models.SmallIntegerField()
    text = models.TextField(null=True, blank=True)
    image = models.ImageField(upload_to= 'comments/', null=True, blank= True)
    like = models.PositiveIntegerField(default= 0)
    dislike = models.PositiveIntegerField(default= 0)

    def __str__(self) -> str:
        return f"{self.customer_id} / {self.product_id}"


class GeneralFeaturesCatalogue(models.Model):
    general_feature_name = models.CharField(max_length= 100)

    def __str__(self) -> str:
        return self.general_feature_name


class ProductGeneralFeature(models.Model):
    product_id = models.ForeignKey(Product, on_delete= models.CASCADE)
    gen_feature_key = models.ForeignKey(GeneralFeaturesCatalogue, on_delete= models.RESTRICT)
    gen_feature_value = models.CharField(max_length= 255)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['product_id', 'gen_feature_key'], name='unique general feature')
    ]

    def __str__(self) -> str:
        return f"{self.product_id} / {self.gen_feature_key} / {self.gen_feature_value}"


class SpecialFeaturesCatalogue(models.Model):
    special_feature_name = models.CharField(max_length= 100)

    def __str__(self) -> str:
        return self.special_feature_name


class SpecialValuesCatalogue(models.Model):
    feature_key = models.ForeignKey(SpecialFeaturesCatalogue, on_delete= models.CASCADE)
    feature_value = models.CharField(max_length= 255)

    def __str__(self) -> str:
        return f"{self.feature_value}"


class ProductSpecialFeature(models.Model):
    sup_pr_detail_id = models.ForeignKey('SupplierProductDetail', on_delete= models.CASCADE)
    spe_feature_key = models.ForeignKey(SpecialFeaturesCatalogue, on_delete= models.CASCADE)
    spe_feature_value = models.ForeignKey(SpecialValuesCatalogue, on_delete= models.CASCADE)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['sup_pr_detail_id', 'spe_feature_key'], name='unique special feature')
    ]

    def __str__(self) -> str:
        return f"{self.sup_pr_detail_id} / {self.spe_feature_key} / {self.spe_feature_value}"


class SupplierProductItem(models.Model):
    supplier = models.ForeignKey(Supplier, on_delete= models.CASCADE)
    product = models.ForeignKey(Product, on_delete= models.CASCADE)

    class Meta:
        constraints = [
        models.UniqueConstraint(fields=['supplier', 'product'], name='unique product for supplier')
    ]

    def __str__(self) -> str:
        return f"{self.supplier} / {self.product}"


class SupplierProductDetail(models.Model):
    sup_pr_item_id = models.ForeignKey(SupplierProductItem, on_delete= models.CASCADE)
    price_per_unit = models.PositiveIntegerField(default=0)
    available_quantity = models.PositiveIntegerField(default=0)
    last_update_date_time = models.DateTimeField(auto_now= True)

    def __str__(self) -> str:
        return f"{self.sup_pr_item_id} / {self.price_per_unit}"    

