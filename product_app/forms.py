from django import forms
from .models import Category, Brand, Review

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

    

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'comment']

        widgets = {
            'rating': forms.Select(choices=[
                (1, '1 - Poor'),
                (2, '2 - Fair'),
                (3, '3 - Good'),
                (4, '4 - Very Good'),
                (5, '5 - Excellent')
            ], attrs={'class': 'form-control'}),
            
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience...'
            })
        }

        labels = {
            'rating': 'Rating',
            'comment': 'Your Review'
        }