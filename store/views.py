from django.shortcuts import render, redirect

from .forms import AddProductForms
from .models import Store, Product


# Create your views here.
def get_store_page(request):
    stores = Store.objects.all()
    print(f"stores -> {stores}")
    print(f"prd -> {Product.objects.all().query}")
    products = Product.objects.all()
    context = {
        'stores': stores,
        'products': products,
    }
    return render(request, 'my_main_page.html', context)


def get_add_product_page(request):
    print("get_add_product_page\n\n\n\n")
    print(request.method)
    stores = Store.objects.all()
    products = Product.objects.all()
    form = AddProductForms()
    if request.method == 'POST':
        form = AddProductForms(request.POST)
        if form.is_valid():
            new_product = Product(**form.cleaned_data)
            new_product.save()
            return redirect('home')
        print(request.POST)
    context = {
        'stores': stores,
        'products': products,
        'form': form,
    }

    return render(request, "add_product.html", context)
