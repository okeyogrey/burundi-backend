from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse
from django.urls import reverse
from django.conf import settings
from django.contrib import messages
from django.db import transaction
from django.db.models import F

from .models import Order, OrderItem
from product_app.models import Product


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


@login_required
@transaction.atomic
def checkout(request):
    cart = request.session.get('cart', {})
    if not cart:
        messages.error(request, "Your cart is empty.")
        return redirect('orders:cart_detail')

    if request.method == 'POST':
        # Validate stock availability
        products_to_update = []
        for key, item in cart.items():
            product = get_object_or_404(Product, pk=item['product_id'])
            if item['quantity'] > product.stock:
                messages.error(request, f"Not enough stock for {product.name}. Available: {product.stock}.")
                return redirect('orders:cart_detail')
            products_to_update.append((product, item['quantity'], key))

        # Create order and deduct stock atomically
        order = Order.objects.create(
            user=request.user,
            paid=True,
            phone_number=request.POST.get('phone_number', '').strip(),
            mpesa_transaction_id=request.POST.get('mpesa_transaction_id', '').strip(),
            benoti_phone_number=request.POST.get('benoti_phone_number', '').strip(),
            benoti_transaction_id=request.POST.get('benoti_transaction_id', '').strip(),
            pickup_location=request.POST.get('pickup_location', '').strip(),
        )

        for product, qty, key in products_to_update:
            OrderItem.objects.create(
                order=order,
                product=product,
                price=product.price,
                quantity=qty,
                size=cart[key].get('size', '')
            )
            # Decrement stock
            Product.objects.filter(pk=product.pk).update(stock=F('stock') - qty)

        # Clear cart
        del request.session['cart']
        messages.success(request, "Order placed successfully!")
        return redirect('orders:order_success', pk=order.pk)

    total_price = sum(i['price'] * i['quantity'] for i in cart.values())
    context = {
        'cart_items': cart.values(),
        'total_price': total_price,
        'PAYSTACK_PUBLIC_KEY': settings.PAYSTACK_PUBLIC_KEY,
    }
    return render(request, 'orders/checkout.html', context)


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


class OrderHistoryView(LoginRequiredMixin, ListView):
    model = Order
    template_name = 'orders/order_history.html'
    context_object_name = 'orders'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user).order_by('-created')


class OrderDetailView(LoginRequiredMixin, DetailView):
    model = Order
    template_name = 'orders/order_detail.html'
    context_object_name = 'order'

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)


def order_success(request, pk):
    """
    Simple thank‑you page after checkout.
    """
    order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_success.html', {
        'order': order
    })
