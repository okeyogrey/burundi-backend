# product_app/templatetags/currency_filters.py
from django import template
from product_app.utils import convert_price  # wherever your function is
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter
def convert_currency(price, currency='KES'):
    # Dummy logic, update based on real rates or session
    if currency == 'BIF':
        return price * 60  # Example conversion rate
    return price



@register.simple_tag
def star_rating(rating, max_stars=5):
    """
    Renders ★/☆ stars for a numeric rating.
    Usage: {% star_rating review.rating %}
    """
    try:
        r = int(rating)
    except (ValueError, TypeError):
        r = 0
    filled = '★' * min(r, max_stars)
    empty  = '☆' * max(0, max_stars - r)
    return mark_safe(filled + empty)