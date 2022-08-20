from django.urls import path

from .views import new_order_payment, return_payment

urlpatterns = [
    path('new-order-payment/<int:order_id>/<int:payment_type_id>',new_order_payment,name='new_order_payment'),
    path('return-payment/',return_payment,name='return_payment'),
    # path('check-payment/<pk>',check_payment,name='check_payment')
]
