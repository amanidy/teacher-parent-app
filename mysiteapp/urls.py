# urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('register/', views.register_user, name='register_user'),
    path('home/', views.base, name='index'), 
    path('messages/', views.messages_view, name='messages'),
    path('progress_updates/', views.progress_updates_view, name='progress_updates'),
    path('meetings/', views.meetings_view, name='meetings'),
    path('logout/', views.logout_view, name='logout'),
]
