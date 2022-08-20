from django.contrib import admin

from .models import Customer, Supplier, CustomerAddress, CustomerFavoriteCategory, NewsLetterSubscriber, Wallet

# Register your models here.
admin.site.register(Customer)
admin.site.register(Supplier)
admin.site.register(CustomerAddress)
admin.site.register(CustomerFavoriteCategory)
admin.site.register(NewsLetterSubscriber)
admin.site.register(Wallet)
