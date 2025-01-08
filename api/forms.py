from django import forms
from .models import CustomUser
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'date_of_birth', 'hobbies', 'password1', 'password2']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hobbies': forms.Textarea(attrs={'rows': 3}),
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'date_of_birth', 'hobbies']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
            'hobbies': forms.Textarea(attrs={'rows': 3}),
        } 
