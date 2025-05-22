from django import forms
from .models import Category, Subcategory, SubSubcategory, Size, Brand, Review

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

    # Field now shows sub‑subcategories; we'll override the display label below
    sub_subcategories = forms.ModelMultipleChoiceField(
        queryset=SubSubcategory.objects.none(),
        required=False,
        widget=forms.CheckboxSelectMultiple,
        label="Sub‑Subcategories"
    )

    # Filter sizes and brands by sub‑subcategory association
    sizes = forms.ModelMultipleChoiceField(
        queryset=Size.objects.all(),
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
        main_category = kwargs.pop('main_category', None)
        super().__init__(*args, **kwargs)
        
        # Override the label for each sub_subcategory instance to display only its name.
        self.fields['sub_subcategories'].label_from_instance = lambda obj: obj.name

        if main_category:
            # Get sub‑subcategories where the parent subcategory belongs to the selected main category.
            self.fields['sub_subcategories'].queryset = SubSubcategory.objects.filter(subcategory__category=main_category)
            self.fields['sizes'].queryset = Size.objects.filter(sub_subcategory__subcategory__category=main_category)
            self.fields['brands'].queryset = Brand.objects.filter(sub_subcategory__subcategory__category=main_category)
        else:
            self.fields['sub_subcategories'].queryset = SubSubcategory.objects.none()
            self.fields['sizes'].queryset = Size.objects.none()
            self.fields['brands'].queryset = Brand.objects.none()

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

class CartAddForm(forms.Form):
    size = forms.ModelChoiceField(
        queryset=Size.objects.none(),
        empty_label=None,
        widget=forms.RadioSelect,
        label=''
    )
    quantity = forms.IntegerField(
        min_value=1,
        initial=1,
        widget=forms.NumberInput(attrs={'class': 'quantity-input', 'style': 'width:60px;'}),
        label=''
    )

    def __init__(self, *args, product=None, **kwargs):
        self.product = product  # Store the product instance for later validation
        super().__init__(*args, **kwargs)
        if product:
            self.fields['size'].queryset = product.sizes.all()

    def clean_quantity(self):
        quantity = self.cleaned_data['quantity']
        if self.product and quantity > self.product.stock:
            raise forms.ValidationError(f"Only {self.product.stock} item(s) in stock.")
        return quantity
