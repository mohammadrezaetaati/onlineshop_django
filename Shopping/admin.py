from django.contrib import admin
from User.models import Customer,Supplier
from Shopping.models import Product,Category,Brands,Feature,FeatureKey,Comment,Discount, ProductFeature,OrderItem,Order,Address

class ProductFeatureInline(admin.StackedInline):
    model = ProductFeature


class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductFeatureInline,
    ]


admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Brands)
admin.site.register(Feature)
admin.site.register(FeatureKey)
admin.site.register(Comment)
admin.site.register(Discount)
admin.site.register(OrderItem)
admin.site.register(Order)
admin.site.register(Address)