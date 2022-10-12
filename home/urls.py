from django.contrib import admin
from django.urls import path, include
from home import views

urlpatterns = [
    path('', views.interview, name='home' ),
    path('schedule', views.schedule, name='schedule'),
    # path('edit', views.edit, name='edit'),
    # path('interviews',views.allInterviews,name='xyz'),
    # path('participants',views.allParticipants,name='participants')
]