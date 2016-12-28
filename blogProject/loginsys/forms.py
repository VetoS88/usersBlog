from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField
from django.contrib.auth.models import User


class ExtUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Email", max_length=254)

    class Meta:
        model = User
        fields = ("username", "email")
        field_classes = {'username': UsernameField}
