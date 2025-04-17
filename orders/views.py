from django.shortcuts import render, redirect
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.conf import settings

def cart_detail(request):
    """
    Display the current session-based cart in detail.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0.0

    for key, item in cart.items():
        subtotal = item['price'] * item['quantity']
        total_price += subtotal
        item['subtotal'] = subtotal
        item['key'] = key  # attach key for removal
        cart_items.append(item)

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'orders/cart_detail.html', context)

def remove_from_cart(request):
    """
    Remove an item from the session-based cart.
    """
    if request.method == 'POST':
        item_key = request.POST.get('item_key')
        if item_key:
            cart = request.session.get('cart', {})
            if item_key in cart:
                del cart[item_key]
                request.session['cart'] = cart
                if request.META.get('HTTP_X_REQUESTED_WITH', '').lower() == 'xmlhttprequest':
                    total_items = sum(item['quantity'] for item in cart.values())
                    return JsonResponse({'message': 'Item removed', 'cart_count': total_items})
    return redirect('orders:cart_detail')

def checkout(request):
    """
    Display the checkout page with current cart details.
    """
    cart = request.session.get('cart', {})
    if not cart:
        return redirect('orders:cart_detail')

    total_price = sum(item['price'] * item['quantity'] for item in cart.values())
    context = {
        'cart_items': cart.values(),
        'total_price': total_price,
        'PAYSTACK_PUBLIC_KEY': settings.PAYSTACK_PUBLIC_KEY,  # Added for Paystack integration
    }
    return render(request, 'orders/checkout.html', context)

def update_cart_quantity(request):
    """
    AJAX endpoint to update the quantity of an item in the cart.
    """
    if request.method == 'POST' and request.is_ajax():
        key = request.POST.get('item_key')
        try:
            qty = int(request.POST.get('quantity', 1))
        except ValueError:
            return JsonResponse({'error': 'Invalid quantity'}, status=400)

        cart = request.session.get('cart', {})
        if key in cart and qty > 0:
            cart[key]['quantity'] = qty
            request.session['cart'] = cart

            subtotal = cart[key]['price'] * qty
            total = sum(item['price'] * item['quantity'] for item in cart.values())
            return JsonResponse({
                'message': 'Quantity updated',
                'subtotal': f"{subtotal:.2f}",
                'total_price': f"{total:.2f}",
                'cart_count': sum(i['quantity'] for i in cart.values()),
            })
    return JsonResponse({'error': 'Bad request'}, status=400)

def process_payment(request):
    """
    Handle the creation of a payment request.
    """
    if request.method == 'POST':
        total_price = request.POST.get('amount')
        # Payment logic integration can be added here
        return redirect('orders:payment_success')  # Dummy redirection for now
    else:
        return redirect('orders:checkout')

def payment_verify(request):
    """
    Verify payment based on reference returned by Paystack.
    """
    reference = request.GET.get('reference')
    # Normally, you would verify the reference with Paystack's API here
    return HttpResponse(f"Payment verified with reference: {reference}")
