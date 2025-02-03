# coding=utf-8
from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name',)  # Customize the fields to display in the admin list view
    search_fields = ('username', 'email', 'first_name', 'last_name')  # Customize the fields to search for

admin.site.register(models.User, UserAdmin)

@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'phone', 'nation', 'position', 'org',]

'''
# method 1

@admin.register(ModelName)
class ModelNameAdmin(admin.ModelAdmin):
    list_display = ['field1', 'field2',]

# method 2

admin.site.register(models.User)
'''
