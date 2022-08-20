from django.http import HttpRequest
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from decouple import config
from idpay.api import IDPayAPI

from cart_shipment.models import Order
from .models import PaymentRecord, PaymentRecordDetail


def payment_init():
    base_url = config('BASE_URL', default='http://127.0.0.1:8000', cast=str)
    api_key = config('IDPAY_API_KEY', default='4d0036f7-207b-484f-a8a1-dd8c38d1262c', cast=str)
    sandbox = config('IDPAY_SANDBOX', default=True, cast=bool)

    return IDPayAPI(api_key, base_url, sandbox)


@login_required(login_url='/login')
def new_order_payment(request:HttpRequest, order_id, payment_type_id):
    
    order = Order.objects.get(id=order_id)
    payment_record = PaymentRecord(order=order, type_id=payment_type_id)
    payment_record.save()

    if payment_type_id == 1:
        idpay_payment = payment_init()
        result = idpay_payment.payment(str(payment_record.id), int(order.total_price)*10, '/payment/return-payment/')

        if 'id' in result:
            PaymentRecordDetail.objects.create(record=payment_record, record_detail_key_id=1, record_detail_value=result['id'])
            PaymentRecordDetail.objects.create(record=payment_record, record_detail_key_id=2, record_detail_value=order.total_price)
            PaymentRecordDetail.objects.create(record=payment_record, record_detail_key_id=3, record_detail_value='1')
            return redirect(result['link'])


@csrf_exempt
def return_payment(request):
    status = request.POST.get('status')
    track_id = request.POST.get('track_id')
    payment_id = request.POST.get('id')
    record_id = request.POST.get('order_id')
    amount = request.POST.get('amount')
    amount = amount[:len(amount)-1]
    card_no = request.POST.get('card_no')
    hashed_card_no = request.POST.get('hashed_card_no')
    generation_date = request.POST.get('date')

    saved_payment_id = PaymentRecordDetail.objects\
        .filter(record_id=record_id,record_detail_key_id=1, record_detail_value=payment_id).first()
    saved_amount = PaymentRecordDetail.objects\
        .filter(record_id=record_id,record_detail_key_id=2, record_detail_value=amount).first()
    saved_status:PaymentRecordDetail = PaymentRecordDetail.objects\
        .filter(record_id=record_id,record_detail_key_id=3, record_detail_value='1').first()
    existing_track_id:PaymentRecordDetail = PaymentRecordDetail.objects\
        .filter(record_detail_key_id=4, record_detail_value=track_id).exists()

    if saved_payment_id and saved_amount and saved_status and not existing_track_id:
 
        saved_status.record_detail_value = status
        saved_status.save()
        PaymentRecordDetail.objects\
            .create(record_id=record_id, record_detail_key_id=4, record_detail_value=track_id)
        PaymentRecordDetail.objects\
            .create(record_id=record_id, record_detail_key_id=5, record_detail_value=card_no)
        PaymentRecordDetail.objects\
            .create(record_id=record_id, record_detail_key_id=6, record_detail_value=hashed_card_no)
        PaymentRecordDetail.objects\
            .create(record_id=record_id, record_detail_key_id=7, record_detail_value=generation_date)

        if status == '10':
            idpay_payment = payment_init()
            result = idpay_payment.verify(payment_id, record_id)
            if 'status' in result:

                    saved_status.record_detail_value = str(result['status'])
                    saved_status.save()
                    PaymentRecordDetail.objects.\
                        create(record_id=record_id, record_detail_key_id=8,\
                        record_detail_value=result['payment']['track_id'])
                    PaymentRecordDetail.objects.\
                        create(record_id=record_id, record_detail_key_id=9,\
                        record_detail_value=result['payment']['date'])
                    PaymentRecordDetail.objects.\
                        create(record_id=record_id, record_detail_key_id=10,\
                        record_detail_value=result['verify']['date'])

                    if saved_status.record_detail_value == '100':
                        payment_record:PaymentRecord = PaymentRecord.objects.get(id=record_id)
                        payment_record.order.deliverystatus_set.create(catalogue_id_id=2)
                        messages.success(request, 'با تشکر از خرید شما. پرداخت سفارش شما تائید گردید و در نوبت پردازش و ارسال قرار گرفت.')
        else:
            messages.error(request, 'متاسفانه پرداخت سفارش شما با خطا مواجه شد و تکمیل نگردید. با توجه به متغیر بودن قیمت و موجودی کالاها، سفارش شما حداکثر به مدت 90 دقیقه برای شما رزرو میگردد تا نسبت به پرداخت آن اقدام فرمایید. با احترام در صورت عدم پرداخت در این بازه زمانی سفارش به صورت خودکار لغو میگردد.')
    return redirect('show_customer_orders')