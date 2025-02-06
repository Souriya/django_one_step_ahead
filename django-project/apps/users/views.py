import logging
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_http_methods
from django.views.decorators.cache import never_cache
from django_ratelimit.decorators import ratelimit

from . import forms
from . import models


logger = logging.getLogger(__name__)

@method_decorator(never_cache, name='dispatch')
@method_decorator(ratelimit(key='header:X-Forwarded-For', rate='1000/10m', block=True), name='dispatch')
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


@never_cache
@require_http_methods(["GET", "POST"])
@ratelimit(key='header:X-Forwarded-For', rate='1000/10m', block=True)
def logout_view(request):
    logout(request)
    messages.success(request, "You have been successfully logged out.")
    return redirect('users:login')


@login_required
@ratelimit(key='header:X-Forwarded-For', rate='1000/10m', block=True)
def home(request):
    context = {
        'title': 'Home',
    }

    template = 'home.html'
    return render(request, template, context)
