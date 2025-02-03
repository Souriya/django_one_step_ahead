from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.conf import settings

from . import models


class LoginForm(forms.Form):
    '''form for user login to continue making appointment'''
    email = forms.EmailField(max_length=100)
    phone = forms.CharField(max_length=100)


class UserRegistrationForm(forms.ModelForm):
    # custom fields to be used along side some
    # fields that we will inherit from User model
    password = forms.CharField(label='Password')
    password2 = forms.CharField(label='Confirm Password')

    phone = forms.CharField()
    nation = forms.CharField()
    position = forms.CharField()
    org = forms.CharField()

    class Meta:
        model = models.User  # we inherit from User model in
        # django.contrib.auth framework
        fields = ('first_name', 'last_name', 'username', 'email',
                'password', 'password2', 'phone', 'nation', 'position', 'org'
        )
        # we take only some fields from the model, not all.

    # check if password and the confirm password are match
    def clean_password2(self):
        # clearn_<fieldname>() is a method used to clean and validate
        # a certain field
        # clean() method is for cleaning the entire form
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError(
                'Passwords don\'t match')
        return cd['password2']


class UserSearchForm(forms.Form):

    search = forms.CharField(max_length=100)
    options = forms.ChoiceField(choices=[('1', 'Name'), ('2', 'Email'), ('3', 'Nation'),
        ('4', 'Position'), ('5', 'Oranization'), ('6', 'Phone')]
    )
