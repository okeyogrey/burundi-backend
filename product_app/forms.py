from django import forms
from .models import Category, Brand, Review

# Sorting choices
SORT_CHOICES = [
    ('-created_at', 'Newest'),
    ('price', 'Price: Low to High'),
    ('-price', 'Price: High to Low'),
]

class ProductFilterForm(forms.Form):
    search_query = forms.CharField(
        required=False,
        label="Search",
        widget=forms.TextInput(attrs={
            'placeholder': 'Search products...',
            'class': 'filter-input',
            'id': 'searchQuery'
        })
    )
    categories = forms.ModelMultipleChoiceField(
        queryset=Category.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    brands = forms.ModelMultipleChoiceField(
        queryset=Brand.objects.all(),
        required=False,
        widget=forms.CheckboxSelectMultiple
    )
    min_price = forms.DecimalField(
        required=False,
        label="Min Price",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Min Price',
            'class': 'filter-input'
        })
    )
    max_price = forms.DecimalField(
        required=False,
        label="Max Price",
        widget=forms.NumberInput(attrs={
            'placeholder': 'Max Price',
            'class': 'filter-input'
        })
    )
    sale_items = forms.BooleanField(
        required=False,
        label="On Sale",
        widget=forms.CheckboxInput(attrs={'class': 'filter-checkbox'})
    )
    sort_by = forms.ChoiceField(
        required=False,
        choices=SORT_CHOICES,
        widget=forms.Select(attrs={'class': 'filter-select'})
    )

    def __init__(self, *args, **kwargs):
        # Pop the main_category if passed, otherwise None
        main_category = kwargs.pop('main_category', None)
        super().__init__(*args, **kwargs)

        if main_category:
            # Show only subcategories of main_category
            self.fields['categories'].queryset = Category.objects.filter(parent=main_category)
        else:
            # No main_category => show no categories
            self.fields['categories'].queryset = Category.objects.none()

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['rating', 'content']

        widgets = {
            'rating': forms.Select(choices=[
                (1, '1 - Poor'),
                (2, '2 - Fair'),
                (3, '3 - Good'),
                (4, '4 - Very Good'),
                (5, '5 - Excellent')
            ], attrs={'class': 'form-control'}),
            
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience...'
            })
        }

        labels = {
            'rating': 'Rating',
            'content': 'Your Review'
        }
