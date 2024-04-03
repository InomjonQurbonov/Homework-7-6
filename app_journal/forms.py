from django import forms
from django.contrib.auth.models import User


class RegistrationForm(forms.ModelForm):
    email = forms.EmailField(label='Email Address', required=True)  # Add email field

    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'username', 'email', 'password')
        widgets = {
            'password': forms.PasswordInput(attrs={'placeholder': 'Enter password'}),
        }
