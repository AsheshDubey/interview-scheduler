import imp
from django.shortcuts import render
from django.views.generic import ListView
from .models import Participant, Interview

# Create your views here.
def interview(request):
    return render(request, 'interview.html')

def schedule(request):
    return render(request, 'schedule.html')

def edit(request):
    return render(request, 'edit.html')