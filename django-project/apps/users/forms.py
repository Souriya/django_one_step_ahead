from django import forms
from django.forms import ModelForm
from django.conf import settings
from django.contrib.auth.forms import AuthenticationForm

from . import models

class LoginForm(forms.Form):
    username = forms.CharField(max_length=100, label="Username / Email / Phone Number")
    password = forms.CharField(widget=forms.PasswordInput)
