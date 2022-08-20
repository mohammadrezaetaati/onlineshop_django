from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.core import validators
from django.contrib.auth import authenticate, get_user_model, password_validation, validators as validators_
from django.utils.translation import gettext_lazy as _


from .models import Customer, Supplier



class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری خود را وارد نمایید'}),
        label='نام کاربری'
    )

    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا کلمه عبور خود را وارد نمایید'}),
        label='کلمه ی عبور'
    )

    def clean_username(self):
        username = self.cleaned_data.get('username')
        is_exists_user = User.objects.filter(username=username).exists()
        if not is_exists_user:
            raise forms.ValidationError('کاربری با مشخصات وارد شده ثبت نام نکرده است')

        return username


class CustomerRegisterForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری خود را وارد نمایید'}),
        label='نام کاربری',
        validators=[
            validators_.UnicodeUsernameValidator(
                message= 'لطفا نام کاربری معتبر وارد نمایید. نام کاربری میتواند بین 8 تا 20 کاراکتر و شامل حروف، اعداد و کاراکترهای @ . + - _ باشد'),
            validators.MaxLengthValidator(limit_value=20,
                message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(limit_value=8, 
                message = 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید'}),
        label='آدرس ایمیل',
        validators=[
            validators.EmailValidator(message= 'آدرس ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    password1 = forms.CharField(
        label=_("رمز عبور"),
        strip=False,
        widget= forms.PasswordInput(attrs={'placeholder': 'لطفا کلمه عبور خود را وارد نمایید'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label=_("تکرار رمز عبور"),
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا تکرار کلمه عبور خود را وارد نمایید'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Customer
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'gender']
        labels = {
            "phone_number" : "شماره تلفن همراه",
            "gender" : "جنسیت"
        }

        widgets = {
            "phone_number" : forms.TextInput(attrs={'placeholder': 'لطفا شماره تلفن خود را وارد نمایید'}),
        }


    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists_user_by_email = User.objects.filter(email=email).exists()
        if is_exists_user_by_email:
            raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')

        if len(email) > 40:
            raise forms.ValidationError('تعداد کاراکترهای ایمیل باید کمتر از 40 باشد')

        return email

    def clean_username(self):
        user_name = self.cleaned_data.get('username')
        is_exists_user_by_username = User.objects.filter(username=user_name).exists()

        if is_exists_user_by_username:
            raise forms.ValidationError('این کاربر قبلا ثبت نام کرده است')

        return user_name

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password2



class SupplierRegisterForm(UserCreationForm):

    username = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا نام کاربری خود را وارد نمایید'}),
        label='نام کاربری',
        validators=[
            validators_.UnicodeUsernameValidator(
                message= 'لطفا نام کاربری معتبر وارد نمایید. نام کاربری میتواند بین 8 تا 20 کاراکتر و شامل حروف، اعداد و کاراکترهای @ . + - _ باشد'),
            validators.MaxLengthValidator(limit_value=20,
                message='تعداد کاراکترهای وارد شده نمیتواند بیشتر از 20 باشد'),
            validators.MinLengthValidator(limit_value=8, 
                message = 'تعداد کاراکترهای وارد شده نمیتواند کمتر از 8 باشد')
        ]
    )

    email = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'لطفا ایمیل خود را وارد نمایید'}),
        label='آدرس ایمیل',
        validators=[
            validators.EmailValidator(message= 'آدرس ایمیل وارد شده معتبر نمیباشد')
        ]
    )

    password1 = forms.CharField(
        label=_("رمز عبور"),
        strip=False,
        widget= forms.PasswordInput(attrs={'placeholder': 'لطفا کلمه عبور خود را وارد نمایید'}),
        help_text=password_validation.password_validators_help_text_html(),
    )

    password2 = forms.CharField(
        label=_("تکرار رمز عبور"),
        widget=forms.PasswordInput(attrs={'placeholder': 'لطفا تکرار کلمه عبور خود را وارد نمایید'}),
        strip=False,
        help_text=_("Enter the same password as before, for verification."),
    )

    class Meta:
        model = Supplier
        fields = ['username', 'email', 'password1', 'password2', 'phone_number', 'address']
        labels = {
            "phone_number" : "شماره تلفن همراه",
            "address" : "آدرس پستی فروشنده"
        }

        widgets = {
            "phone_number" : forms.TextInput(attrs={'placeholder': 'لطفا شماره تلفن خود را وارد نمایید'}),
            "address" : forms.Textarea(attrs={'placeholder': 'لطفا آدرس پستی محل کار خود را وارد نمایید'}),

        }


    def clean_email(self):
        email = self.cleaned_data.get('email')
        is_exists_user_by_email = User.objects.filter(email=email).exists()
        if is_exists_user_by_email:
            raise forms.ValidationError('ایمیل وارد شده تکراری میباشد')

        if len(email) > 40:
            raise forms.ValidationError('تعداد کاراکترهای ایمیل باید کمتر از 40 باشد')

        return email

    def clean_username(self):
        user_name = self.cleaned_data.get('username')
        is_exists_user_by_username = User.objects.filter(username=user_name).exists()

        if is_exists_user_by_username:
            raise forms.ValidationError('این کاربر قبلا ثبت نام کرده است')

        return user_name

    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 != password2:
            raise forms.ValidationError('کلمه های عبور مغایرت دارند')

        return password2