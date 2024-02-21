from django.shortcuts import render

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
    return render(request,'my_main_page.html', context)

def get_add_product_page(request):
    # products = Product.objects.get(id=)
    stores = Store.objects.all()
    products = Product.objects.all()
    form = AddProductForms()
    context = {
        'stores': stores,
        'products': products,
        'form': form,
    }

    return render(request, "add_product.html",context)