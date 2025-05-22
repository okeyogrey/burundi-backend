from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse

from .models import (
    Product, Review, Category, Subcategory, SubSubcategory,
    Brand, Size
)
from .forms import ProductFilterForm, ReviewForm, CartAddForm



def set_currency(request, currency):
    """
    Simple view to switch between 'KES' and 'BIF'.
    Stores choice in session and redirects back.
    """
    if currency in ('KES', 'BIF'):
        request.session['currency'] = currency
    return redirect(request.META.get('HTTP_REFERER', 'product_app:landing_page'))



def product_list(request):
    main_cat_id = request.GET.get('main_category')
    # Updated parameter name for sub‑subcategories
    sub_subcat_ids = request.GET.getlist('sub_subcategories')

    main_category = None
    if main_cat_id:
        try:
            main_category = Category.objects.get(pk=main_cat_id)
        except Category.DoesNotExist:
            main_category = None

    products = Product.objects.all().order_by('-created_at')
    if main_category:
        products = products.filter(category=main_category)
    if sub_subcat_ids:
        products = products.filter(sub_subcategory__id__in=sub_subcat_ids)

    form = ProductFilterForm(request.GET, main_category=main_category)
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            products = products.filter(name__icontains=search_query)

        sizes = form.cleaned_data.get('sizes')
        if sizes:
            products = products.filter(sizes__in=sizes).distinct()

        brands = form.cleaned_data.get('brands')
        if brands:
            products = products.filter(brand__in=brands)

        min_price = form.cleaned_data.get('min_price')
        if min_price is not None:
            products = products.filter(price__gte=min_price)

        max_price = form.cleaned_data.get('max_price')
        if max_price is not None:
            products = products.filter(price__lte=max_price)

        sale_items = form.cleaned_data.get('sale_items')
        if sale_items:
            products = products.filter(is_on_sale=True)

        sort_by = form.cleaned_data.get('sort_by')
        if sort_by:
            products = products.order_by(sort_by)

    paginator = Paginator(products, 6)
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






def convert_price(price, currency):
    # Example conversion rates: adjust as needed
    if currency == 'BIF':
        return price * 30  # example rate from KES to BIF
    return price  # default is KES, no conversion

def product_list_json(request):
    main_cat_id = request.GET.get('main_category')
    sub_subcat_ids = request.GET.getlist('sub_subcategories')

    main_category = None
    if main_cat_id:
        try:
            main_category = Category.objects.get(pk=main_cat_id)
        except Category.DoesNotExist:
            main_category = None

    currency = request.session.get("currency", "KES")

    products = Product.objects.all().order_by('-created_at')
    if main_category:
        products = products.filter(category=main_category)
    if sub_subcat_ids:
        products = products.filter(sub_subcategory__id__in=sub_subcat_ids)

    form = ProductFilterForm(request.GET, main_category=main_category)
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            products = products.filter(name__icontains=search_query)

        sizes = form.cleaned_data.get('sizes')
        if sizes:
            products = products.filter(sizes__in=sizes).distinct()

        brands = form.cleaned_data.get('brands')
        if brands:
            products = products.filter(brand__in=brands)

        min_price = form.cleaned_data.get('min_price')
        if min_price is not None:
            products = products.filter(price__gte=min_price)

        max_price = form.cleaned_data.get('max_price')
        if max_price is not None:
            products = products.filter(price__lte=max_price)

        sale_items = form.cleaned_data.get('sale_items')
        if sale_items:
            products = products.filter(is_on_sale=True)

        sort_by = form.cleaned_data.get('sort_by')
        if sort_by:
            products = products.order_by(sort_by)

    paginator = Paginator(products, 9)
    page = request.GET.get('page')
    try:
        products_page = paginator.page(page)
    except PageNotAnInteger:
        products_page = paginator.page(1)
    except EmptyPage:
        products_page = paginator.page(paginator.num_pages)

    data = []
    for product in products_page:
        price_converted = convert_price(product.price, currency)
        old_price_converted = convert_price(product.old_price, currency) if product.old_price else None

        data.append({
            'id': product.id,
            'name': product.name,
            'price': round(price_converted, 0),
            'old_price': round(old_price_converted, 0) if old_price_converted else None,
            'image_url': product.image.url if product.image else '',
            'is_on_sale': product.is_on_sale
        })
    return JsonResponse({'products': data})








def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
    if request.user.is_authenticated:
        existing_review = reviews.filter(user=request.user).exists()
    else:
        existing_review = False

    review_form = ReviewForm()
    cart_form = CartAddForm(product=product)

    if request.method == 'POST':
        if 'add_to_cart' in request.POST:
            cart_form = CartAddForm(request.POST, product=product)
            if cart_form.is_valid():
                cd = cart_form.cleaned_data
                size = cd.get('size')
                quantity = cd.get('quantity')
                size_value = size.pk if hasattr(size, 'pk') else str(size)
                cart = request.session.get('cart', {})
                key = f"{product.id}_{size_value}"
                if key in cart:
                    cart[key]['quantity'] += quantity
                else:
                    cart[key] = {
                        'product_id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'size': size_value,
                        'quantity': quantity,
                        'image_url': product.image.url if product.image else ''
                    }
                request.session['cart'] = cart
                messages.success(request, f"Added {quantity} item(s) of {product.name} to your cart.")

                ajax_header = request.META.get('HTTP_X_REQUESTED_WITH', '')
                if 'xmlhttprequest' in ajax_header.lower():
                    total_items = sum(item['quantity'] for item in cart.values())
                    return JsonResponse({'message': 'Item added to cart', 'cart_count': total_items})
                return redirect('product_app:product_detail', product_id=product.id)
        elif 'buy_now' in request.POST:
            cart_form = CartAddForm(request.POST, product=product)
            if cart_form.is_valid():
                cd = cart_form.cleaned_data
                size = cd.get('size')
                quantity = cd.get('quantity')
                size_value = size.pk if hasattr(size, 'pk') else str(size)
                cart = request.session.get('cart', {})
                key = f"{product.id}_{size_value}"
                if key in cart:
                    cart[key]['quantity'] += quantity
                else:
                    cart[key] = {
                        'product_id': product.id,
                        'name': product.name,
                        'price': float(product.price),
                        'size': size_value,
                        'quantity': quantity,
                        'image_url': product.image.url if product.image else ''
                    }
                request.session['cart'] = cart
                messages.success(request, f"Added {quantity} item(s) of {product.name} to your cart.")
                return redirect('product_app:product_detail', product_id=product.id)
        elif 'submit_review' in request.POST:
            review_form = ReviewForm(request.POST)
            if review_form.is_valid():
                review = review_form.save(commit=False)
                review.product = product
                review.user = request.user
                review.save()
                messages.success(request, 'Your review has been submitted successfully!')
                return redirect('product_app:product_detail', product_id=product.id)

    context = {
        'product': product,
        'reviews': reviews,
        'form': review_form,
        'existing_review': existing_review,
        'related_products': related_products,
        'cart_form': cart_form,
    }
    return render(request, 'product_app/product_detail.html', context)


def landing_page(request):
    categories = Category.objects.all().order_by('name')
    featured_products = Product.objects.filter(is_on_sale=True)[:8]

    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'product_app/landing.html', context)


def search_products(request):
    query = request.GET.get('search_query','').strip()
    results = []
    if query:
        matching_products = Product.objects.filter(name__icontains=query)[:5]
        for product in matching_products:
            results.append({
                'id': product.id,
                'name': product.name,
                'detail_url': f'/product/{product.id}/'
            })
    return JsonResponse({'products': results})
