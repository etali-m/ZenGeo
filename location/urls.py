from django.urls import path
from . import views

from django.urls import path, re_path 

urlpatterns = [
    path('', views.index, name='home')
]