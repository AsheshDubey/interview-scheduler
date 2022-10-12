from email.policy import default
from enum import unique
from operator import truediv
from xmlrpc.client import Fault
from django.db import models

# Create your models here.

class Candidate(models.Model):
    name = models.CharField(max_length=122)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.name

class Slot(models.Model):
    interview_date = models.DateField(null=True)
    start_time = models.TimeField(null=True)
    end_time = models.TimeField(null=True)

    def __str__(self):
        return str(self.id)

class Schedule(models.Model):
    slot = models.ForeignKey("Slot", on_delete=models.CASCADE)
    candidate = models.ForeignKey("Candidate", on_delete=models.CASCADE)

    def __str__(self):
        return str(self.candidate.name) 