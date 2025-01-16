from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Hobby


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user, extending the default UserCreationForm.
    Includes additional fields: date_of_birth and hobbies.
    """
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'name', 'date_of_birth', 'hobbies']


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating an existing user, extending the default UserChangeForm.
    Includes additional fields: date_of_birth and hobbies.
    """
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name', 'date_of_birth', 'hobbies']
