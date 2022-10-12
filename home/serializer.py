from rest_framework.serializers import ModelSerializer
from .models import Interview, Participant

class InterviewSerializer(ModelSerializer):
    class Meta:
        model = Interview
        fields = "__all__"

class ParticipantSerializer(ModelSerializer):
    class Meta:
        model = Participant
        fields = "__all__"