from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address')
        
        # We add an 'aria-label' for accessibility
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Username',
                'aria-label': 'Username'  # For screen readers
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Email Address',
                'aria-label': 'Email Address' # For screen readers
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'Phone Number (e.g., 0712345678)',
                'aria-label': 'Phone Number' # For screen readers
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Delivery Address',
                'aria-label': 'Delivery Address', # For screen readers
                'rows': 3
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if 'username' in self.fields:
            self.fields['username'].help_text = ''
        
        # Add placeholders and aria-labels to the password fields
        if 'password' in self.fields:
            self.fields['password'].widget.attrs.update({
                'placeholder': 'Password',
                'aria-label': 'Password'
            })
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs.update({
                'placeholder': 'Confirm Password',
                'aria-label': 'Confirm Password'
            })