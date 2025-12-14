from django.contrib import admin
from django.urls import path, include
from . import views


urlpatterns = [
    path('', views.home, name='home'),
    path('cpp', views.cpp, name='cpp'),
    path('java', views.java, name='java'),
    path("share/<uuid:uid>/", views.view_shared_code),
]