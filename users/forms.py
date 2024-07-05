from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User

class SignupForm(UserCreationForm):
    confirm_password = forms.CharField(max_length=255, widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('user_type', 'first_name', 'last_name', 'profile_picture', 'username', 'email', 'password1', 'password2', 'address_line1', 'city', 'state', 'pincode')

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 != password2:
            raise forms.ValidationError("Passwords do not match")
        return cleaned_data