from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from .models import Product, Review, Category
from .forms import ProductFilterForm, ReviewForm

def product_list(request):
    # 1. Identify main_category from query string
    main_cat_id = request.GET.get('main_category')
    main_category = None
    if main_cat_id:
        try:
            main_category = Category.objects.get(pk=main_cat_id)
        except Category.DoesNotExist:
            main_category = None

    # 2. Base queryset
    products = Product.objects.all().order_by('-created_at')

    # 3. Filter products by main_category if valid
    if main_category:
        products = products.filter(category=main_category)

    # 4. Pass main_category to ProductFilterForm
    form = ProductFilterForm(request.GET, main_category=main_category)

    # 5. Additional filters if form is valid
    if form.is_valid():
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            products = products.filter(name__icontains=search_query)

        subcategories = form.cleaned_data.get('subcategories')
        print("DEBUG: Selected subcategories =>", subcategories)
        if subcategories:
            products = products.filter(subcategory__in=subcategories)
        print("DEBUG: Final products after subcategory filter =>", products)

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

    # 6. Pagination
    paginator = Paginator(products, 6)
    page = request.GET.get('page')
    try:
        products = paginator.page(page)
    except PageNotAnInteger:
        products = paginator.page(1)
    except EmptyPage:
        products = paginator.page(paginator.num_pages)

    # Pass the entire query string so we can preserve it in the template
    context = {
        'products': products,
        'form': form,
        'request_get': request.GET.urlencode()  # e.g. "main_category=20&search_query=something"
    }
    return render(request, 'product_app/product_list.html', context)


def product_list_json(request):
    """Return filtered products as JSON (for AJAX)."""
    main_cat_id = request.GET.get('main_category')
    main_category = None
    if main_cat_id:
        try:
            main_category = Category.objects.get(pk=main_cat_id)
        except Category.DoesNotExist:
            main_category = None

    products = Product.objects.all().order_by('-created_at')

    if main_category:
        products = products.filter(category=main_category)

    form = ProductFilterForm(request.GET, main_category=main_category)
    if form.is_valid():
        print("DEBUG: subcategories raw =>", request.GET.getlist('subcategories'))
        search_query = form.cleaned_data.get('search_query')
        if search_query:
            products = products.filter(name__icontains=search_query)

        subcategories = form.cleaned_data.get('subcategories')
        print("DEBUG: subcategories from cleaned_data =>", subcategories)
        if subcategories:
            products = products.filter(subcategory__in=subcategories)
            print("DEBUG: final SQL =>", products.query)
            print("DEBUG: final product list =>", list(products))
        
        print("DEBUG: final subcategory filter SQL =>", products.query)
        print("DEBUG: final product list =>", list(products))

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

    # 6. PAGINATION FOR AJAX (9 items per page, as you have)
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


@login_required
def product_detail(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    reviews = Review.objects.filter(product=product)
    related_products = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
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
