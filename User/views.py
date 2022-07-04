from multiprocessing import context
import random

from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login,logout as logout_
from django.views import View
from django.views.generic import CreateView
from django.core.cache import cache
from django.db import transaction

from .form import CustomerCreationForm,SupplierCreationForm,SendSmsForm,LoginReceivedCodeForm,SendEmailForm,RegisterForm\
    ,ProfileForm,ChangePasswordForm
from . models import Customer, Supplier, User
from .tasks import send_email,sendsms



def login_rgister_page(request,):
        if request.method=="GET":
            return render(request,'login2.html')
        if request.method=="POST":
            password = request.POST['password']
            user = authenticate(request,username=request.session.get('email'), password=password)
            print(user)
            if user:
                login(request, user)
                return redirect('/')
    
class Register(View):
    
    def get(self, request):
        form=RegisterForm()
        return render(request,'register.html',context={'form':form})
    def post(self,request):
        form=RegisterForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                user=User.objects.create(phone_number=request.session.get('phonenumber'),email=request.session.get('email'))
                user.set_password(form.cleaned_data["password1"])
                if form.cleaned_data.get('status')=='customer':
                    user.is_customer=True
                    Customer.objects.create(user=user)
                else:
                    user.is_suplier=True
                    Supplier.objects.create(user=user)
                user.save()
                return redirect('/')
        return render(request,'register.html',context={'form':form})
    
    
        
        

    # if request.method=='POST':
    #     username=request.POST['username']
    #     password = request.POST['password']
    #     user = authenticate(request, username=username, password=password)
    #     if user: 
    #         login(request, user)
    #         return redirect('/')
       
    #     else:
    #         context={
    #             'error':user
    #         }
    #         print(user)
    #         return render(request,'login2.html',context)
    # return render(request,'login2.html')


class RegisterCstomer(CreateView):

    model=User
    form_class=CustomerCreationForm
    template_name='register.html'
    success_url='/login/'


class RegisterSupplier(RegisterCstomer):

    form_class=SupplierCreationForm
    template_name='register_supplier.html'
    

def send_code(request,email=None,phonenumber=None):
    code=random.randint(1000,9999)
    if email:
        cache.set(email,code,60*2)
        send_email.delay(email,code)
        session=request.session['email']=email 
        print(code)
        return session
    elif phonenumber: 
        cache.set(phonenumber,code,60*2)
        sendsms.delay(phonenumber,code)
        session=request.session['phonenumber']=phonenumber
        print(code)
        return session

        
def ckeck_code(request,code,email=False,phonenumber=False):
    if email:
        session=request.session.get('email')
        code_cash=cache.get(session)
    elif phonenumber:
        session=request.session.get('phonenumber')
        code_cash=cache.get(session)
        # login(request,session)
    return code_cash==code


class LoginSendEmail(View):

    def get(self,request):
        form=SendEmailForm()
        return render(request,'login_email.html',context={'form':form})
    def post(self, request):
        form=SendEmailForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            request.session['email']=email 
            if User.objects.filter(email=email).exists():
                    return redirect('/login/')
            return render(request,'checkout.html')
            send_code(request,email)
            # return redirect('/login_received_code/')  
            

        return render(request,'login_email.html',context={'form':form})

class LoginSendSms(View):

    def get(self,request):
        form=SendSmsForm()
        return render(request,'login_sms.html',context={'form':form})
    def post(self,request):
        form=SendSmsForm(request.POST)
        if form.is_valid():
            phonenumber=form.cleaned_data.get('phone_number')
            request.session['phonenumber']=phonenumber
            if User.objects.filter(phone_number=phonenumber).exists():
                return render(request,'login_sms.html',context={'form':form})
            send_code(request,phonenumber=phonenumber)
            return redirect('/login_received_code/')  
        return render(request,'login_sms.html',context={'form':form})

class LoginReceivedCode(View):

    def get(self,request):
        form=LoginReceivedCodeForm()
        return render(request,'login_received_code.html',context={'form':form})

    def post(self,request):
        form=LoginReceivedCodeForm(request.POST)
        print(request.POST)
        if form.is_valid():
            code=form.cleaned_data.get('code')
            if ckeck_code(request,code,email=True):
                return redirect('/sendsms_login/')
            if ckeck_code(request,code,phonenumber=True):
                return redirect('/register/')
                # return redirect('/')
        return render(request,'login_received_code.html',context={'form':form})

class Profile(View):

    def get(self,request):
        user:User=User.objects.get(email=request.session.get('email'))
        form=ProfileForm(request.GET)
        context={
            'user':user
        }
        return render(request,'my-account.html',context)
        
    def post(self,request):
        form=ProfileForm(request.POST)
        if form.is_valid(): 
            firstname=form.cleaned_data.get('first_name')
            lastname=form.cleaned_data.get('last_name')
            email=form.cleaned_data.get('email')
            User.objects.filter(email=request.session.get('email'))\
                .update(first_name=firstname,last_name=lastname,email=email)
        return render(request,'my-account.html')

class ChangePassword(View):

    def post(self,request):
        form=ChangePasswordForm(request.POST)
        if form.is_valid():
            password=form.cleaned_data.get('password')
            new_password=form.cleaned_data.get('new_password')
            conf_password=form.cleaned_data.get('conf_password')
            print(request.session.get('email'),'kkkkkkkkkkkkkkkkkkkkkkkkk')
            user:User=User.objects.get(email=request.session.get('email'))
            if user.check_password(password):
                if new_password==conf_password:
                    user.set_password(conf_password)
                    user.save()
                    user_login = authenticate(request,username=request.session.get('email'), password=conf_password)
                    login(request, user_login)
                    request.session['email']=user.email
                    return redirect('/profile/')
        return render(request,'my-account.html')

     
def logout(request):
    logout_(request)
    return redirect('/')

