from django.urls import path

from .views import RegisterCstomer,RegisterSupplier,login_rgister_page,logout,\
    LoginReceivedCode,LoginSendSms,LoginSendEmail,Register,Profile,ChangePassword


urlpatterns = [
    path('login/', login_rgister_page,name='login'),
    path('register/', Register.as_view(),name='register'),
    path('register_customer/', RegisterCstomer.as_view() ,name='register_customer'),
    path('register_supplier/', RegisterSupplier.as_view() ,name='register_supplier'),
    path('sendsms_login/', LoginSendSms.as_view() ,name='sendsms_login'),
    path('sendemail_login/', LoginSendEmail.as_view() ,name='sendemail_login'),
    path('login_received_code/', LoginReceivedCode.as_view() ,name='login_received_code'),
    path('profile/', Profile.as_view() ,name='profile'),
    path('profile-changepassword/', ChangePassword.as_view() ,name='changepassword'),
    path('logout/', logout,name='logout'),
]
