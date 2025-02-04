# coding=utf-8
from django.db import models
from django.conf import settings
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    AbstractUser,
)


phone_regex = RegexValidator(
    regex=r"^\d{8}$",  # Exactly 8 digits
    message=_("Phone number must be 8 digits."), # _() allow text to be translated
)


class User(AbstractUser):
    '''custom user model inherited from default User model'''

    # add phone number as extra field
    phone_number = models.CharField(max_length=8, unique=True, validators=[phone_regex],  # Use the regex validator
        error_messages={
            "unique": _("A user with that phone number already exists."),
        },
    )
    # change email to be unique too, default django auth allow duplicated email address
    email = models.EmailField(max_length=60, unique=True,  # Make email unique
        error_messages={
            "unique": _("A user with that email address already exists."),
        },
    )
    # now when create an user account, it requires username, phone and email
    REQUIRED_FIELDS = ["email", "phone_number"]  # Email, phone number are now required

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.phone_number})"


class Profile(models.Model):
    '''user profile link to User, every user account has one associated profile'''

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    theme_color = models.CharField(max_length=50, blank=True, null=True, default='w3-theme-blue.css')

    def __str__(self):
        return 'Profile of {}'.format(self.user.phone_number)

    def user_email(self):
        return self.user.email


'''
# model snipet

class ModelName(models.Model):

    field1 = models.CharField(blank=True, max_length=300)
    field2 = models.CharField(blank=True, max_length=300)

    class Meta:
        verbose_name = 'Model Name'
        verbose_name_plural = 'Model Names'
        ordering = ['field1']
        indexes = [
            models.Index(fields=['field1']),
        ]

    def __str__(self):
        return self.field1
'''
