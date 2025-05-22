# product_app/templatetags/rating_tags.py
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.simple_tag
def star_rating(rating, max_stars=5):
    """
    Renders a string of ★ and ☆ up to max_stars.
    Usage: {% star_rating review.rating %}
    """
    try:
        r = int(rating)
    except (ValueError, TypeError):
        r = 0
    filled = '★' * min(r, max_stars)
    empty  = '☆' * max(0, max_stars - r)
    return mark_safe(filled + empty)
