"""
URL configuration for apps project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# django core libs
from django.contrib import admin
from django.urls import path, include

# 3rd party libs
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path('admin12321/', admin.site.urls), # change default admin path to reduce bruteforce
    path('api-auth/',
         include('rest_framework.urls', namespace='rest_framework')),
    path(
        'api/schema/',
        SpectacularAPIView.as_view(),
        name='api-schema'),
    path(
        'api/docs/',
        SpectacularSwaggerView.as_view(url_name='api-schema'),
        name='api-docs'),
    path(
        'api/redocs/',
        SpectacularRedocView.as_view(url_name='api-schema'),
        name='api-redocs'
    ),
    path('',
        include('users.urls', namespace='users')
    ),
]

'''
    path('new_app/',
        include('custom_apps.new_app.urls', namespace='new_app')
    ),
'''
