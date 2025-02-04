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
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)  # Re-render the form with errors message

    def form_valid(self, form):
        form_data = form.cleaned_data
        user = authenticate(self.request, username=form_data['username'], password=form_data['password'])

        if user is not None: # if we can find the user
            if user.is_active: # if user status is active
                login(self.request, user)
                return redirect('users:home')  # Redirect on success to /home/
            else:
                messages.error(self.request, "Your account is inactive.")  # Inactive account
                return super().form_invalid(form)
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
