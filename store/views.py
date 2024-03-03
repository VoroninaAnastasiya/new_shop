from django.shortcuts import render, redirect

from .forms import AddProductForms
from .models import Store, Product


# Create your views here.
def get_store_page(request):
    stores = Store.objects.all()
    products = Product.objects.all()
    context = {
        'stores': stores,
        'products': products,
    }
    return render(request, 'my_main_page.html', context)


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
            print(request.POST)
        else:
            print(form.errors)


    context = {
        'stores': stores,
        'products': products,
        'form': form,
    }

    return render(request, "add_product.html", context)


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
        'store': store,
        'products': products,
    }
    return render(request, 'get_all_zara_products.html', context)


def get_product_info(request):
    product = Product.objects.get()