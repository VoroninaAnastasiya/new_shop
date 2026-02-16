from django.contrib.auth import login
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect

from .forms import AddProductForms, AuthForm, AuthRegisterForm
from .models import Store, Product


# Create your views here.
# переписать на классы все методы


def get_store_page(request):
    stores = Store.objects.all()
    products = Product.objects.all()
    context = {
        'stores': stores,
        'products': products,
    }
    print(request.user)
    return render(request, 'my_main_page.html', context)


# это уходит с главной страницы в профиль для авторизационных пользователей с ролью менеджер
def get_add_product_page(request):
    stores = Store.objects.all()
    products = Product.objects.all()
    form = AddProductForms()
    if request.method == 'POST':
        form = AddProductForms(request.POST, request.FILES)
        if form.is_valid():
            new_product = Product(**form.cleaned_data)
            new_product.save()
            return redirect('home')
        else:
            print(form.errors)


    context = {
        'stores': stores,
        'products': products,
        'form': form,
    }

    return render(request, "add_product.html", context)

# сделать один метод по фильтрации товаров по названиям продуктов из get_all_lichi_products и get_all_zara_products, плюс пагинация
def get_all_lichi_products(request, id):
    products = Product.objects.filter(store=id)
    context = {
        'products': products,
    }
    return render(request, 'get_all_lichi_products.html', context)

def get_all_zara_products(request):
    store = Store.objects.get(id=3)
    products = Product.objects.filter(store=store.id).all()
    context = {
        'brand': store,
        'products': products,
    }
    return render(request, 'get_all_zara_products.html', context)


# переписать на jwt авторизацию
def auth_login(request):
    form = AuthForm()
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            user = form.authenticate_user()
            login(request, user)
            return redirect('home')

    return render(request, 'auth.html', {'form': form})


# переписать на jwt авторизацию
def register(request):
    form = AuthRegisterForm()
    if request.method == 'POST':
        form = AuthRegisterForm(request.POST)
        if form.is_valid():
            User.objects.create_user(**form.cleaned_data)
            return redirect('home')

    context = {
        'form': form,
    }

    return render(request, "register.html", context)
