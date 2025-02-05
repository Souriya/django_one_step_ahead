import logging
from django_ratelimit.decorators import ratelimit
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache

from . import forms
from . import models

logger = logging.getLogger(__name__)


@method_decorator(never_cache, name='dispatch')
#@ratelimit(key='ip', rate='100/m', block=True)
class Login(LoginView):
    '''user login using class base view (CBV)'''

    form_class = AuthenticationForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get the default context provided by LoginView
        context['title'] = 'Login'  # Add custom context
        context['theme_color'] = 'w3-theme-blue.css'
        return context

    def get_success_url(self):
        return reverse_lazy('users:home')

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)  # Re-render the form with errors message


@method_decorator(never_cache, name='dispatch')
#@ratelimit(key='ip', rate='100/m', block=True)
class Login2(LoginView):
    '''user login using class base view (CBV)'''

    form_class = forms.LoginForm
    template_name = 'login.html'
    redirect_authenticated_user = True

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)  # Get the default context provided by LoginView
        context['title'] = 'Login'  # Add custom context
        context['theme_color'] = 'w3-theme-blue.css'
        return context

    def get_success_url(self):
        return reverse_lazy('users:home')

    def form_invalid(self, form):
        messages.error(self.request, "Invalid username or password.")
        return super().form_invalid(form)  # Re-render the form with errors message

    '''
    AxesBackendRequestParameterRequired at /login/ AxesBackend requires a request as an argument to authenticate
    AxesBackend is not receiving the request object it needs to function properly. need to ensure that the request
    object is passed to the authentication backend make it work.
    '''
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def dispatch(self, request, *args, **kwargs):
        self.request = request
        return super().dispatch(request, *args, **kwargs)


@method_decorator(never_cache, name='dispatch')
def login(request):
    context = {
        'title': 'Login',
        'form': forms.LoginForm,
        'theme_color': 'w3-theme-red.css',
    }

    template = 'login-old.html'
    return render(request, template, context)


@method_decorator(never_cache, name='dispatch')
#@ratelimit(key='ip', rate='20/m', method=['GET', 'POST'], block=True)
class Logout(LogoutView):
    '''logout using CBV'''
    next_page = reverse_lazy('users:login')  # Redirect to login page after logout


def home(request):
    context = {
        'title': 'Home',
    }

    template = 'home.html'
    return render(request, template, context)
