from django.contrib import admin

from .models import Cart, CartItem, Order, OrderItem, DeliveryType, DeliveryStatus\
    , DeliveryStatusCatalogue

# Register your models here.
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(DeliveryType)
admin.site.register(DeliveryStatus)
admin.site.register(DeliveryStatusCatalogue)
