from django.urls import path

from .views import login_,logout_, customer_register, supplier_register

urlpatterns = [
    path('login/', login_, name= 'login'),
    path('logout/',logout_, name= 'logout'),
    path('customer-register/', customer_register, name= 'customer_register'),
    path('supplier-register/', supplier_register, name= 'supplier_register'),
]
