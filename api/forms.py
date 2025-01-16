from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Hobby


class CustomUserCreationForm(UserCreationForm):
    """
    Form for creating a new user, extending the default UserCreationForm.
    Includes additional fields: date_of_birth, existing hobbies, and new hobbies.
    """
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False
    )
    existing_hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Select Existing Hobbies"
    )
    new_hobbies = forms.CharField(
        widget=forms.TextInput(attrs={'placeholder': 'Add hobbies separated by commas'}),
        required=False,
        label="Add New Hobbies"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'password1', 'password2', 'email', 'name', 'date_of_birth', 'existing_hobbies', 'new_hobbies']

    def save(self, commit=True):
        user = super().save(commit=False)

        print("Saving user:", user.username)
        print("Existing hobbies:", self.cleaned_data.get('existing_hobbies'))
        print("New hobbies:", self.cleaned_data.get('new_hobbies'))

        if commit:
            user.save()

            # Handle existing hobbies
            existing_hobbies = self.cleaned_data.get('existing_hobbies') or []  # Default to empty list
            if existing_hobbies:
                user.user_hobbies.add(*existing_hobbies)

            # Handle new hobbies
            new_hobbies = self.cleaned_data.get('new_hobbies', "")
            if new_hobbies.strip():
                hobby_names = [h.strip() for h in new_hobbies.split(',') if h.strip()]
                for hobby_name in hobby_names:
                    hobby, _ = Hobby.objects.get_or_create(name=hobby_name)
                    user.user_hobbies.add(hobby)

        return user



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
