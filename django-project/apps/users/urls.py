from django.urls import path, include
from . import views

# 3rd party libs
from rest_framework.routers import DefaultRouter

# from . import views

app_name = 'users' # Namespace for URLs in this users app
router = DefaultRouter()
# router.register('', views.ViewSet)

urlpatterns = [
    path('home/', views.home, name='home'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('api/', include(router.urls)),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
