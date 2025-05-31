from decimal import Decimal

def convert_price(price, currency):
    if currency == 'BIF':
        return price * Decimal('60.00')  # use string to avoid float precision errors
    return price
