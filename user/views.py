from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout

from .forms import LoginForm, CustomerRegisterForm, SupplierRegisterForm

# Create your views here
def login_(request):
    if request.user.is_authenticated:
        return redirect('/')

    login_form = LoginForm(request.POST or None)
    print('login form:', login_form)
    if login_form.is_valid():
        print('clean data:', login_form.cleaned_data)
        username = login_form.cleaned_data.get('username')
        password = login_form.cleaned_data.get('password')
        user = authenticate(request, username=username, password=password)
        print('user:', user)
        if user:
            login(request, user)
            return redirect('/')
        else:
            login_form.add_error('username', 'کاربری با مشخصات وارد شده یافت نشد')

    context = {
        'login_form': login_form
    }
    return render(request, 'user/login.html', context)


def logout_(request):
    logout(request)
    return redirect('/')


def customer_register(request):
    if request.user.is_authenticated:
        return redirect('/')
    register_form = CustomerRegisterForm(request.POST or None)

    if register_form.is_valid():
        register_form.save()
        return redirect('/login')
        
    context = {
        'register_form': register_form
    }
    return render(request, 'user/customer_register.html', context)


def supplier_register(request):
    if request.user.is_authenticated:
        return redirect('/')
    register_form = SupplierRegisterForm(request.POST or None)

    if register_form.is_valid():
        register_form.save()
        return redirect('/login')
        
    context = {
        'register_form': register_form
    }
    return render(request, 'user/supplier_register.html', context)