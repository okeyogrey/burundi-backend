from django.conf import settings

def cart_counter(request):
    cart = request.session.get('cart', {})
    count = sum(item['quantity'] for item in cart.values())
    return {'cart_count': count}

def currency(request):
    """
    Injects:
      - current_currency: either 'KES' or 'BIF'
      - currency_rate: hard-coded 60
      - convert_price(): callable to apply the rate
    """
    current = request.session.get('currency', 'KES')
    rate = 60

    def convert(amount):
        if current == 'BIF':
            return amount * rate
        return amount

    return {
        'current_currency': current,
        'currency_rate': rate,
        'convert_price': convert,
    }
