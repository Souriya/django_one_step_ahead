# coding=utf-8
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    AbstractUser,
)

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


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

#    def create_superuser(self, email, password=None, **extra_fields):
#        extra_fields.setdefault('is_staff', True)
#        extra_fields.setdefault('is_superuser', True)

#        if password is None:
#            raise ValueError('Superusers must have a password.')

#        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):

    name = models.CharField(blank=True, max_length=100)
    last_name = models.CharField(blank=True, max_length=100)
    email = models.EmailField(unique=True, max_length=100)
    phone = models.CharField(blank=True, max_length=100)
    nationality = models.CharField(blank=True, max_length=100)
    position = models.CharField(blank=True, max_length=100)
    org = models.CharField(blank=True, max_length=100)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
#    PASSWORD_FIELD = 'phone'
