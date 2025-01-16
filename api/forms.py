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
        required=False,
        label="Date of Birth"
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

    def clean_new_hobbies(self):
        """
        Validate the new hobbies field to ensure proper formatting and length.
        """
        new_hobbies = self.cleaned_data.get('new_hobbies', "")
        if new_hobbies.strip():
            hobby_names = [h.strip() for h in new_hobbies.split(',') if h.strip()]
            if any(len(h) > 255 for h in hobby_names):  # Assuming the max length of a hobby name is 255
                raise forms.ValidationError("Hobby names must be less than 255 characters.")
        return new_hobbies

    def save(self, commit=True):
        """
        Save the user and associate hobbies (both existing and new).
        """
        try:
            user = super().save(commit=False)

            if commit:
                user.save()

                # Handle existing hobbies
                existing_hobbies = self.cleaned_data.get('existing_hobbies') or []
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
        except Exception as e:
            raise forms.ValidationError(f"An error occurred while saving hobbies: {str(e)}")


class CustomUserChangeForm(UserChangeForm):
    """
    Form for updating an existing user, extending the default UserChangeForm.
    Includes additional fields: date_of_birth and hobbies.
    """
    date_of_birth = forms.DateField(
        widget=forms.DateInput(attrs={'type': 'date'}),
        required=False,
        label="Date of Birth"
    )
    hobbies = forms.ModelMultipleChoiceField(
        queryset=Hobby.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Hobbies"
    )

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'name', 'date_of_birth', 'hobbies']

    def save(self, commit=True):
        """
        Save the user and update hobbies.
        """
        try:
            user = super().save(commit=False)

            if commit:
                user.save()

                # Update hobbies
                hobbies = self.cleaned_data.get('hobbies', [])
                if hobbies:
                    user.user_hobbies.set(hobbies)  # Updates the ManyToMany field

            return user
        except Exception as e:
            raise forms.ValidationError(f"An error occurred while updating hobbies: {str(e)}")
