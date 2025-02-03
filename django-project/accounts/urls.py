from django.urls import path, include
from . import views

# 3rd party libs
from rest_framework.routers import DefaultRouter

# from . import views

app_name = 'core'
router = DefaultRouter()
# router.register('', views.ViewSet)

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.user_login, name='login'),
    path('login_fail/', views.login_fail, name='login_fail'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('user_register_2554189632521/', views.user_register, name='user_register'),
    path('user_list/', views.user_list, name='user_list'),
    path('user_search/', views.user_search, name='user_search'),
    path('user_detail/<int:id>', views.user_detail, name='user_detail'),
    path('request_meeting/<int:destination_id>/<int:time_slot>', views.request_meeting, name='request_meeting'),
    path('request_meeting_save/<int:destination_id>/<int:time_slot>/<int:location>',
        views.request_meeting_save, name='request_meeting_save'),
    path('request_meeting_accept_decline/<int:schedule_id>/<int:request_status_id>',
        views.request_meeting_accept_decline, name='request_meeting_accept_decline'),

    path('api/', include(router.urls)),
]

# when user go to path /app_name/ it will show api root page (endpoints list)
urlpatterns += router.urls
