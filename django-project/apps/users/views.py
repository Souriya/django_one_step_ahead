import logging
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.core.cache import cache
from django.ratelimit.decorators import ratelimit

from . import forms
from . import models

logger = logging.getLogger(__name__)

# Constants related to the number of login fail
FAILED_LOGIN_ATTEMPTS = 10 # max 10 times fails
BLOCK_DURATION = 60 * 60  # 1 hour in seconds
LOGIN_ATTEMPT_CACHE_KEY_PREFIX = 'login_attempts_'
BLOCK_CACHE_KEY_PREFIX = 'block_'  # New prefix for block status

@method_decorator(never_cache, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='20/m', method=['GET', 'POST']), name='dispatch')
class Login(LoginView):
    '''user login using class base view (CBV)'''

    form_class = forms.LoginForm
    template_name = 'login.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get the default context provided by LoginView
        context['title'] = 'Login'  # Add custom context
        return context

    def form_invalid(self, form):
        ip_address = self.request.META.get('REMOTE_ADDR')
        block_cache_key = f"{BLOCK_CACHE_KEY_PREFIX}{ip_address}"

        if cache.get(block_cache_key):  # If IP is blocked
            messages.error(self.request, "Too many failed login attempts. Your IP has been blocked for 1 hour.")
            return super().form_invalid(form)

        cache_key = f"{LOGIN_ATTEMPT_CACHE_KEY_PREFIX}{ip_address}"
        attempts = cache.get(cache_key, 0)

        if attempts >= FAILED_LOGIN_ATTEMPTS:
            messages.error(self.request, "Too many failed login attempts. Your IP has been blocked for 1 hour.")
            cache.set(block_cache_key, True, timeout=BLOCK_DURATION) # Block the IP
        else:
            messages.error(self.request, "Invalid username or password.")

        return super().form_invalid(form)  # Re-render the form with errors message

    def form_valid(self, form):
        ip_address = self.request.META.get('REMOTE_ADDR')
        block_cache_key = f"{BLOCK_CACHE_KEY_PREFIX}{ip_address}"

        if cache.get(block_cache_key):  # If IP is blocked
            messages.error(self.request, "Too many failed login attempts. Your IP has been blocked for 1 hour.")
            return super().form_invalid(form)

        cache_key = f"{LOGIN_ATTEMPT_CACHE_KEY_PREFIX}{ip_address}"
        form_data = form.cleaned_data
        user = authenticate(self.request, username=form_data['username'], password=form_data['password'])

        if user is not None: # if we can find the user
            if user.is_active: # if user status is active
                login(self.request, user)
                cache.delete(cache_key)  # Reset attempts number on successful login
                return redirect('users:home')  # Redirect on success to /home/
            else:
                messages.error(self.request, "Your account is inactive.")  # Inactive account
                return super().form_invalid(form)
        else:
            attempts = cache.get(cache_key, 0)
            attempts += 1
            cache.set(cache_key, attempts, timeout=60) # Store attempts for 1 minute

            if attempts >= FAILED_LOGIN_ATTEMPTS:
                messages.error(self.request, "Too many failed login attempts. Your IP has been blocked for 1 hour.")
                cache.set(block_cache_key, True, timeout=BLOCK_DURATION)  # Block the IP
            else:
                messages.error(self.request, "Invalid username or password.")

            return super().form_invalid(form)

    def get_success_url(self):
        return reverse_lazy('users:home') # if login success, send user to /home/


@method_decorator(never_cache, name='dispatch')
@method_decorator(ratelimit(key='ip', rate='20/m', method=['GET', 'POST']), name='dispatch')
class Logout(LogoutView):
    '''logout using CBV'''
    next_page = reverse_lazy('users:login')  # Redirect to login page after logout
