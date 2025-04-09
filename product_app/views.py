from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.http import JsonResponse

from .models import (
    Product, Review, Category, Subcategory, SubSubcategory,
    Brand, Size
)
from .forms import ProductFilterForm, ReviewForm

def product_list(request):
    # 1. Identify main_category, subcategories, sub_subcategories from query string (using getlist for multiple values)
    main_cat_id = request.GET.get('main_category')
    subcat_ids = request.GET.getlist('subcategories')  # note: plural in URL
    sub_subcat_ids = request.GET.getlist('sub_subcategory')

    main_category = None
    if main_cat_id:
        try:
            main_category = Category.objects.get(pk=main_cat_id)
        except Category.DoesNotExist:
            main_category = None

    # 2. Base queryset – order by newest first
    products = Product.objects.all().order_by('-created_at')

    # 3. Filter by main_category if provided
    if main_category:
        products = products.filter(category=main_category)

    # 4. Filter by subcategories (GET parameter)
    if subcat_ids:
        products = products.filter(subcategory__id__in=subcat_ids)

    # 5. Filter by sub_subcategories (GET parameter)
    if sub_subcat_ids:
        products = products.filter(sub_subcategory__id__in=sub_subcat_ids)

    # 6. Instantiate the filter form (it is used for additional filters like search, sizes, brand, price, etc.)
    form = ProductFilterForm(request.GET, main_category=main_category)

    # 7. Apply additional filters from the form (but do NOT re-filter subcategories since that’s already done)
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

    # 8. Paginate – 6 items per page
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


def product_list_json(request):
    """Return filtered products as JSON (for AJAX)."""
    main_cat_id = request.GET.get('main_category')
    subcat_ids = request.GET.getlist('subcategories')
    sub_subcat_ids = request.GET.getlist('sub_subcategory')

    main_category = None
    if main_cat_id:
        try:
            main_category = Category.objects.get(pk=main_cat_id)
        except Category.DoesNotExist:
            main_category = None

    products = Product.objects.all().order_by('-created_at')
    if main_category:
        products = products.filter(category=main_category)
    if subcat_ids:
        products = products.filter(subcategory__id__in=subcat_ids)
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
        data.append({
            'id': product.id,
            'name': product.name,
            'price': float(product.price),
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


def landing_page(request):
    """
    A view that shows a landing page (like Jumia’s homepage) with a mega menu.
    """
    categories = Category.objects.all().order_by('name')
    featured_products = Product.objects.filter(is_on_sale=True)[:8]

    context = {
        'categories': categories,
        'featured_products': featured_products,
    }
    return render(request, 'product_app/landing.html', context)
