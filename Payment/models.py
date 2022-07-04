from django.db import models

from User.models import Customer, Supplier
from Shopping.models import Product


class PaymentFactor(models.Model):
    CHOICE_STATUS=(
        ('Successful','successful'),
        ('Unsuccessful','unsuccessful'),
    )
    order_detail=models.OneToOneField('OrderDetails', on_delete=models.RESTRICT)
    amount=models.PositiveIntegerField()
    status=models.CharField(max_length=255,choices=CHOICE_STATUS)
    create_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.status

    
class OrderDetails(models.Model):
    customer=models.OneToOneField(Customer, on_delete=models.RESTRICT)
    payment=models.ForeignKey(PaymentFactor,on_delete=models.RESTRICT)
    create_at=models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.payment


class OrderItems(models.Model):
    order_detail=models.ForeignKey(OrderDetails,on_delete=models.RESTRICT)
    product=models.ForeignKey(Product, on_delete=models.RESTRICT)
    create_at=models.DateTimeField(auto_now_add=True)
