from django.shortcuts import render
from .models import Product
from .forms import ProductFilterForm

def product_list(request):
    products = Product.objects.all()
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        if form.cleaned_data['category']:
            products = products.filter(category=form.cleaned_data['category'])

        if form.cleaned_data['brand']:
            products = products.filter(brand=form.cleaned_data['brand'])

        if form.cleaned_data['min_price']:
            products = products.filter(price__gte=form.cleaned_data['min_price'])

        if form.cleaned_data['max_price']:
            products = products.filter(price__lte=form.cleaned_data['max_price'])

        if form.cleaned_data['sale_items']:
            products = products.filter(is_on_sale=True)

    context = {
        'products': products,
        'form': form
    }
    return render(request, 'product_app/product_list.html', context)
