from django.contrib import admin

from .models import Product, Comment, FavoriteProduct, SupplierProductItem\
    , SupplierProductDetail, Category, ProductGeneralFeature, ProductSpecialFeature\
    , GeneralFeaturesCatalogue, SpecialFeaturesCatalogue, SpecialValuesCatalogue

# Register your models here.
admin.site.register(Product)
admin.site.register(Comment)
admin.site.register(FavoriteProduct)
admin.site.register(SupplierProductItem)
admin.site.register(SupplierProductDetail)
admin.site.register(Category)
admin.site.register(ProductGeneralFeature)
admin.site.register(ProductSpecialFeature)
admin.site.register(GeneralFeaturesCatalogue)
admin.site.register(SpecialFeaturesCatalogue)
admin.site.register(SpecialValuesCatalogue)


