from django.urls import path
from . import views

from django.urls import path, re_path 

urlpatterns = [
    path('', views.index, name='home'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
]