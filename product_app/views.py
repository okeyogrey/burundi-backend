from django.shortcuts import render, get_object_or_404, redirect
from .models import Product, Review
from .forms import ProductFilterForm
from .forms import ReviewForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required

def product_list(request):
    products = Product.objects.all().order_by('-created_at')
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


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)

    # Prevent duplicate reviews
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
        'existing_review': existing_review  # Add this if missing
    }
    return render(request, 'product_app/product_detail.html', context)