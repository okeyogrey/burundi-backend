from django import forms
from .models import Category, Brand

class ProductFilterForm(forms.Form):
    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        empty_label="All Categories"
    )
    brand = forms.ModelChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        empty_label="All Brands"
    )
    min_price = forms.DecimalField(
        required=False,
        label="Min Price",
        widget=forms.NumberInput(attrs={'placeholder': 'Min Price'})
    )
    max_price = forms.DecimalField(
        required=False,
        label="Max Price",
        widget=forms.NumberInput(attrs={'placeholder': 'Max Price'})
    )
    sale_items = forms.BooleanField(
        required=False,
        label="On Sale"
    )
