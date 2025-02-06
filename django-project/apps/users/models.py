# coding=utf-8
from django.db import models
from django.conf import settings
from django.utils import timezone
from dateutil.relativedelta import relativedelta
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import (
    AbstractUser,
)


phone_regex = RegexValidator(
    regex=r"^\d{8}$",  # Exactly 8 digits
    message=_("Phone number must be 8 digits."), # _(xxx) allow text to be translated
)


class User(AbstractUser):
    '''custom user model inherited from default User model'''

    class Meta:
        verbose_name = "User"
        verbose_name_plural = "Users"

    # add phone number as extra field
    phone_number = models.CharField(max_length=8, unique=True, validators=[phone_regex],  # Use the regex validator
        null=True, blank=True, error_messages={"unique": _("A user with that phone number already exists."),},)
    # change email to be unique too, default django auth allow duplicated email address
    email = models.EmailField(max_length=60, unique=True,  # Make email unique
        error_messages={"unique": _("A user with that email address already exists."),},)
    # now when create an user account, it requires username, phone and email
    REQUIRED_FIELDS = ["email"]

    date_created = models.DateTimeField(auto_now_add=True)
    date_modified = models.DateTimeField(auto_now=True)
    modified_by = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='modified_users')

    def save(self, *args, **kwargs):
        if not self.pk:  # If this is a new object
            self.date_created = timezone.now()
        self.date_modified = timezone.now()

        # Hash the password if it has been changed
        if not self.pk or not self.password.startswith(('pbkdf2_sha256$', 'bcrypt$', 'argon2')):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.phone_number})"


class Profile(models.Model):
    '''user profile link to User, every user account has one associated profile'''

    class Meta:
        verbose_name = "Profile"
        verbose_name_plural = "Profiles"

    LANGUAGE_CHOICES = [
        ('en', _('English')),
        ('lo', _('Lao')),
    ] # 'en' or 'lo' is the value stored in the databas not English or Lao

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    theme_color = models.CharField(max_length=50, blank=True, null=True, default='w3-theme-blue.css')
    language = models.CharField(max_length=2, choices=LANGUAGE_CHOICES, default='en')

    def __str__(self):
        return 'Profile of {}'.format(self.user.username)

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
