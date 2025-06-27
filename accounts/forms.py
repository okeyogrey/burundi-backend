from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'phone_number', 'address')
        
        # We define the widgets for each field here
        widgets = {
            'username': forms.TextInput(attrs={
                'placeholder': 'Enter your username'
            }),
            'email': forms.EmailInput(attrs={
                'placeholder': 'Enter your email address'
            }),
            'phone_number': forms.TextInput(attrs={
                'placeholder': 'e.g., 0712345678'
            }),
            'address': forms.Textarea(attrs={
                'placeholder': 'Enter your delivery address',
                'rows': 3 # Keeps your original setting for the address field
            }),
        }

    def __init__(self, *args, **kwargs):
        """
        Override the init method to remove the default help text for username
        and to add the 'required' attribute to the password fields.
        """
        super().__init__(*args, **kwargs)
        # The default UserCreationForm includes help text we don't need
        # because we have placeholders now.
        if 'username' in self.fields:
            self.fields['username'].help_text = ''
        
        # The password fields are not in Meta.fields but are added by UserCreationForm.
        # We can add placeholders to them here.
        if 'password' in self.fields:
             self.fields['password'].widget.attrs['placeholder'] = 'Create a password'
        if 'password2' in self.fields:
            self.fields['password2'].widget.attrs['placeholder'] = 'Confirm your password'