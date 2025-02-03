# coding=utf-8
from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import date, datetime
from dateutil.relativedelta import relativedelta
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    AbstractUser,
)


class User(AbstractUser):

    orgs = models.ForeignKey('Organization', on_delete=models.SET_NULL, related_name='org', null=True, blank=True)

class Profile(models.Model):
    # we create user object with 1-to-1 relationship with User model,
    # and we refer to the User model using global setting instead of refer to it directly
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='profile')

    # personal info
    uuid = models.CharField(max_length=30, null=True, blank=True)
    phone = models.CharField(max_length=120, null=True, blank=True)
    nation = models.CharField(max_length=120, null=True, blank=True)
    position = models.CharField(max_length=120, null=True, blank=True)
    org = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return 'Profile of {}'.format(self.user.username)

    def user_email(self):
        return self.user.email


class Organization(models.Model):
    name = models.CharField(max_length=120, blank=True)

    class Meta:
        verbose_name = 'Oraganization'
        verbose_name_plural = 'Oraganizations'

    def __str__(self):
        return self.name


'''
# model snipet

class ModelName(models.Model):

    field1 = models.CharField(blank=True, max_length=300)
    field2 = models.CharField(blank=True, max_length=300)

    class Meta:
        verbose_name = 'Model Name'
        verbose_name_plural = 'Model Names'
        ordering = ['field1']

    def __str__(self):
        return self.field1
'''
