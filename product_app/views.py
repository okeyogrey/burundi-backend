from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.core import serializers

from .models import Product, Review
from .forms import ProductFilterForm, ReviewForm

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
    form = ProductFilterForm(request.GET)

    # Apply filters if form is valid
    if form.is_valid():
        # Search Query
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            products = products.filter(name__icontains=search_query)

        # Multiple Categories
        categories = form.cleaned_data.get('categories')
        if categories:
            products = products.filter(category__in=categories)

        # Multiple Brands
        brands = form.cleaned_data.get('brands')
        if brands:
            products = products.filter(brand__in=brands)

        # Min Price
        min_price = form.cleaned_data.get('min_price')
        if min_price is not None:
            products = products.filter(price__gte=min_price)

        # Max Price
        max_price = form.cleaned_data.get('max_price')
        if max_price is not None:
            products = products.filter(price__lte=max_price)

        # On Sale
        sale_items = form.cleaned_data.get('sale_items')
        if sale_items:
            products = products.filter(is_on_sale=True)

        # Sort By
        sort_by = form.cleaned_data.get('sort_by')
        if sort_by:
            products = products.order_by(sort_by)

    # Pagination Logic
    paginator = Paginator(products, 10)  # Show 10 products per page
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    context = {
        'products': products,
        'form': form
    }
    return render(request, 'product_app/product_list.html', context)

def product_list_json(request):
    """Return filtered products as JSON."""
    products = Product.objects.all().order_by('-created_at')
    form = ProductFilterForm(request.GET)

    if form.is_valid():
        # Search Query
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            products = products.filter(name__icontains=search_query)

        # Categories
        categories = form.cleaned_data.get('categories')
        if categories:
            products = products.filter(category__in=categories)

        # Brands
        brands = form.cleaned_data.get('brands')
        if brands:
            products = products.filter(brand__in=brands)

        # Min Price
        min_price = form.cleaned_data.get('min_price')
        if min_price is not None:
            products = products.filter(price__gte=min_price)

        # Max Price
        max_price = form.cleaned_data.get('max_price')
        if max_price is not None:
            products = products.filter(price__lte=max_price)

        # On Sale
        sale_items = form.cleaned_data.get('sale_items')
        if sale_items:
            products = products.filter(is_on_sale=True)

        # Sort By
        sort_by = form.cleaned_data.get('sort_by')
        if sort_by:
            products = products.order_by(sort_by)

    # Convert queryset to JSON (only fields you need)
    data = []
    for product in products:
        data.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
            'image_url': product.image.url if product.image else '',
            'is_on_sale': product.is_on_sale
        })
    return JsonResponse({'products': data})

@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)

    # Fetch related products (limit 4)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]

    # Prevent duplicate reviews by the same user
    existing_review = reviews.filter(user=request.user).exists()

    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.product = product
            review.user = request.user
            review.save()
            messages.success(request, 'Your review has been submitted successfully!')
            return redirect('product_app:product_detail', product_id=product.id)
    else:
        form = ReviewForm()

    context = {
        'product': product,
        'reviews': reviews,
        'form': form,
        'existing_review': existing_review,
        'related_products': related_products
    }
    return render(request, 'product_app/product_detail.html', context)
