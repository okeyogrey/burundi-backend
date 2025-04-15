from django.shortcuts import render, redirect
from django.contrib import messages

def cart_detail(request):
    """
    Display the current session-based cart.
    """
    cart = request.session.get('cart', {})
    cart_items = []
    total_price = 0.0

    for key, item in cart.items():
        # Compute subtotal for each cart item.
        subtotal = item['price'] * item['quantity']
        total_price += subtotal
        # Optionally add the subtotal to the item dictionary.
        item['subtotal'] = subtotal
        cart_items.append(item)
    
    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'orders/cart_detail.html', context)
