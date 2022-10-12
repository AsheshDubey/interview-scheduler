from django.contrib import admin
from .models import Candidate, Schedule,Slot

# Register your models here.

admin.site.register(Schedule)
admin.site.register(Slot)
admin.site.register(Candidate)