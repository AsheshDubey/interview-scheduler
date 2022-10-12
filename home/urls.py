from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.schedule, name='schedule' ),
    path('schedule', views.schedule, name='schedule'),
]