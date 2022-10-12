from django.contrib import admin
from .models import Participant, Interview, Candidate, Schedule,Slot

# Register your models here.
# admin.site.register(Participant)
# admin.site.register(Interview)
admin.site.register(Schedule)
admin.site.register(Slot)
admin.site.register(Candidate)