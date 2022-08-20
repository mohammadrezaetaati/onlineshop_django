import uuid

from django.db import models

from cart_shipment.models import Order

class PaymentType(models.Model):
    name = models.CharField(max_length= 50)

    def __str__(self):
        return f'{self.name}'


class PaymentTypeDataKey(models.Model):
    type = models.ForeignKey(PaymentType, on_delete= models.RESTRICT)
    data_name = models.CharField(max_length= 50)
    # data_type = models.CharField(max_length= 50)

    def __str__(self):
        return f'{self.id}. {self.type} / {self.data_name}'


class PaymentRecord(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.ForeignKey(Order, on_delete= models.RESTRICT)
    type = models.ForeignKey(PaymentType, on_delete= models.RESTRICT)
    date_time = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        while PaymentRecord.objects.filter(id=self.id).exists():
            self.id = uuid.uuid4()
        return super().save(*args, **kwargs)
    
    def __str__(self):
        return f'{self.order} / {self.type} / {self.id}'


class PaymentRecordDetail(models.Model):
    record = models.ForeignKey(PaymentRecord, on_delete= models.CASCADE)
    record_detail_key = models.ForeignKey(PaymentTypeDataKey, on_delete= models.RESTRICT)
    record_detail_value = models.CharField(max_length= 100)

    def __str__(self):
        return f'{self.record} / {self.record_detail_key} / {self.record_detail_value}'
