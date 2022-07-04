from django.conf import settings
from django.core.mail import send_mail

from celery import shared_task
from kavenegar import *





@shared_task
def sendsms(phonenumber,code):
  
    api = KavenegarAPI('314A3568704B675845556E797047483746684D396D55456F44674473506E49384F6A337A5831776C45376B3D') 
    params = { 'sender' : '10008663', 'receptor': phonenumber, 'message' :f'کدتاییدشما:{code}'} 
    response = api.sms_send( params)


@shared_task
def send_email(email,code):

    subject='code for login:'
    message=f'code:{code}'
    from_email=settings.EMAIL_HOST_USER
    recipient_list=[email]
    send_mail(subject,message,from_email,recipient_list)
