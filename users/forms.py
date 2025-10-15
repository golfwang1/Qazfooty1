# users/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import FanPhoto


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=False, help_text="Необязательно")

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


class UpdateUserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ("username", "email")


class FanPhotoForm(forms.ModelForm):
    class Meta:
        model = FanPhoto
        fields = ["photo", "caption"]  # <-- ВАЖНО: photo, не image
        widgets = {
            "photo": forms.ClearableFileInput(attrs={"accept": "image/*"}),
            "caption": forms.TextInput(attrs={"placeholder": "Короткая подпись"}),
        }

