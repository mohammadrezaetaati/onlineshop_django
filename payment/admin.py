from django.contrib import admin

from .models import PaymentRecord, PaymentRecordDetail, PaymentType, PaymentTypeDataKey

# Register your models here.
admin.site.register(PaymentRecord)
admin.site.register(PaymentRecordDetail)
admin.site.register(PaymentType)
admin.site.register(PaymentTypeDataKey)
