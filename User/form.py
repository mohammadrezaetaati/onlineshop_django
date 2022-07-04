
from dataclasses import fields
from multiprocessing import context
from pyexpat import model
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.password_validation import NumericPasswordValidator
from django.contrib.auth import authenticate, get_user_model, password_validation
from django.core.validators import RegexValidator

from .models import Supplier, User,Customer

# class LoginForm(forms.Form):

#     username=forms.CharField(max_length=100)
#     password=forms.PasswordInput()

class SendSmsForm(forms.Form):

    phone_number = forms.CharField(
    label="",
    max_length=11,
    validators=[RegexValidator(regex='^09\d{9}$',message='شماره تلفن به درستی وارد نشده')],
    widget=forms.TextInput(attrs={'placeholder': 'شماره تلفن'})
    )

class SendEmailForm(forms.Form):

    email = forms.EmailField(
    label="",
    widget=forms.TextInput(attrs={'placeholder': 'ایمیل'})
    )

class LoginReceivedCodeForm(forms.Form):

    code=forms.IntegerField(
        label="",
        validators=[RegexValidator(regex='[0-9]{4}',message='کد تایید به درستی واردنشده!')],
        widget=forms.TextInput(attrs={'placeholder': 'کد'})
        )
    


class CustomerCreationForm(UserCreationForm):

    error_messages = {
            'password_mismatch': 'رمزمطابقت ندارد',
            }
    password1 = forms.CharField(
        label=("Password"),
        strip=False,
        widget=forms.PasswordInput(attrs={'placeholder':'رمزعبور'}),
        help_text=password_validation.password_validators_help_text_html(),
)
    password2 = forms.CharField(
        label=("Password confirmation"),
        widget=forms.PasswordInput(attrs={'placeholder':'تکراررمزعیور'}),
        strip=False,
        help_text=("Enter the same password as before, for verification."),
)
    class Meta:
        model = User
        fields=[
             'email','password1','password2','phone_number','national_id'
        ]

        error_messages = {
            'email': {
                'unique': 'این ایمیل از قبل وارد شده است',
                'required':'پرکردن فیلدالزامی است',
                'invalid':'ایمیل را به درستی وارد کنید'
            },
            'phone_number': {
                'unique': 'این شماره تلفن از قبل وارد شده است',
                'required':'پرکردن فیلدالزامی است'
            },
       
            'national_id': {
                'unique': 'این کدملی از قبل وارد شده است',
                'required':'پرکردن فیلدالزامی است'
            },
        }

        widgets={
            'email': forms.TextInput
                           (attrs={'placeholder':'ایمیل'}),
            'phone_number': forms.TextInput
                           (attrs={'placeholder':'شماره تلقن'}),
            
            'national_id': forms.TextInput
                           (attrs={'placeholder':'کدملی'}),
            'password1': forms.TextInput
                           (attrs={'placeholder':'کدملی'}),
        }
     
    def save(self):
        user= super().save()
        user.is_customer=True
        Customer.objects.create(user=user)
        user.save()
        return user


class RegisterForm(CustomerCreationForm):

    CHOICES_STATUS=[('customer','مشتری'),
                    ('supplier','فروشنده')]

    status = forms.ChoiceField(choices=CHOICES_STATUS, widget=forms.RadioSelect)

    class Meta:
        model=User
        fields=['password1','password2','status']
        


class SupplierCreationForm(CustomerCreationForm):

    shop_name=forms.CharField(
        max_length=30, 
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'نام قروشگاه'}),
        error_messages={'required':'پرکردن فیلدالزامی است'})
 
    class Meta(CustomerCreationForm.Meta):
        
        fields=[
              'email','password1','password2','phone_number','national_id','shop_name',
        ]

    
    def save(self):
        user= super().save()
        user.is_suplier=True
        user.save()
        supplier=Supplier.objects.create(user=user)
        supplier.shop_name=self.cleaned_data.get('shop_name')
        supplier.save()
        return supplier
       

class ProfileForm(forms.Form):
    first_name=forms.CharField()
    last_name=forms.CharField()
    email=forms.EmailField()
 

class ChangePasswordForm(forms.Form):

    password=forms.CharField(widget=forms.PasswordInput,error_messages={'invalid':'ddddddd'})
    new_password=forms.CharField(widget=forms.PasswordInput)
    conf_password=forms.CharField(widget=forms.PasswordInput)

# class ProfileForm(forms.ModelForm):
#     # new_password=forms.CharField(widget=forms.PasswordInput)
#     # conf_password=forms.CharField(widget=forms.PasswordInput)
#     class Meta:
#         model=User
#         fields=['first_name','last_name','email']