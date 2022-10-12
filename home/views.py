import imp
import json
from django.shortcuts import render
from django.views.generic import ListView
from .models import Candidate, Slot, Schedule, Participant, Interview
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import InterviewSerializer, ParticipantSerializer
from django.contrib import messages

def process_query(query):
    ls = query.split("&")
    body = {}

    for i in ls:
        l = i.split("=")
        items = body.get(l[0],[])
        if l[1].isnumeric():
            items.append(int(l[1]))
        else :
            items.append(l[1])
        body[l[0]] = items
    

    return body

# Create your views here.
def interview(request):
    return render(request, 'interview.html')

def schedule(request):

    if request.method =='POST':


        body = process_query(str(request.body.decode()))
        participants = body.get("test")
        interview_date = request.POST.get("date")
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")

        print(participants, start_time, end_time, interview_date)
        ##validations
        if(len(participants)<2):
            match_slot = Schedule.objects.filter(slot__interview_date=interview_date, slot__start_time=start_time, slot__end_time=end_time)
            if(len(match_slot)>0):
                if(len(match_slot.filter(candidate__id=participants[0]))>0):
                    print("this is no no step b")
                    messages.error(request, "Error: This Interview Entry Already Exists!")
                else:
                    match_user = Schedule.objects.filter(candidate__id=participants[0])
                    print(match_user)
                    if(len(match_user)>0):
                        print("invoke step d")
                        match_date = match_user.filter(slot__interview_date=interview_date)
                        if(len(match_date)>0):
                            if((match_date.filter(slot__start_time__gte=end_time) | match_date.filter(slot__end_time__lte=start_time))==True):
                                try:
                                    slot_new = Slot.objects.get(interview_date=interview_date, start_time=start_time, end_time=end_time)
                                except:
                                    slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
                                    slot_new.save()
                        
                                current_paritcipant = Candidate.objects.get(id=participants[0])
                                schedule_current = Schedule.objects.create(slot=slot_new, candidate=current_paritcipant)
                                schedule_current.save()
                                messages.success(request, "Success: Interview Scheduled Successfully!")
                            else:
                                print("this is a no no step d")
                                messages.error(request, "Error: This Participant is not available during the scheduled time!")
                        else:
                            try:
                                slot_new = Slot.objects.get(interview_date=interview_date, start_time=start_time, end_time=end_time)
                            except:
                                slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
                                slot_new.save()
                        
                            current_paritcipant = Candidate.objects.get(id=participants[0])
                            schedule_current = Schedule.objects.create(slot=slot_new, candidate=current_paritcipant)
                            schedule_current.save()
                            messages.success(request, "Success: Interview Scheduled Successfully!")
                    else:
                        print("this is a no no step c")
                        messages.success(request, "Success: Interview Scheduled Successfully!")
                        try:
                            slot_new = Slot.objects.get(interview_date=interview_date, start_time=start_time, end_time=end_time)
                        except:
                            slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
                            slot_new.save()
                        
                        for participant_id in participants:
                            current_paritcipant = Candidate.objects.get(id=participant_id)
                            schedule_current = Schedule.objects.create(slot=slot_new, candidate=current_paritcipant)
                            schedule_current.save()
            else:
                print("this is a no no step a")
                messages.error(request, "Error: Please select atleast two Participants for this slot")
        else:
            total_participants = len(participants)
            print(total_participants)
            feasible_schedules=[]
            for participant_id in participants:
                match_user = Schedule.objects.filter(candidate__id=participant_id)
                print(match_user)
                if(len(match_user)>0):
                    print("invoke step d")
                    match_date = match_user.filter(slot__interview_date=interview_date)
                    if(len(match_date)>0):
                        if((match_date.filter(slot__start_time__gte=end_time) | match_date.filter(slot__end_time__lte=start_time))==True):
                            try:
                                slot_new = Slot.objects.get(interview_date=interview_date, start_time=start_time, end_time=end_time)
                            except:
                                slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
                                slot_new.save()

                            current_paritcipant = Candidate.objects.get(id=participant_id)
                            feasible_schedules.append({'slot_id':slot_new.id, 'candidate_id': current_paritcipant.id})
                        else:
                            print("this is a no no step d")
                            messages.error(request, "Error: This Participant is not available during the scheduled time!")
                    else:
                        try:
                            slot_new = Slot.objects.get(interview_date=interview_date, start_time=start_time, end_time=end_time)
                        except:
                            slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
                            slot_new.save()
                        
                        current_paritcipant = Candidate.objects.get(id=participant_id)
                        feasible_schedules.append({'slot_id':slot_new.id, 'candidate_id': current_paritcipant.id})
                else:
                    print("this is a no no step c")
                    try:
                        slot_new = Slot.objects.get(interview_date=interview_date, start_time=start_time, end_time=end_time)
                    except:
                        slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
                        slot_new.save()
                        
                    current_paritcipant = Candidate.objects.get(id=participant_id)
                    feasible_schedules.append({'slot_id':slot_new.id, 'candidate_id': current_paritcipant.id})

            print(len(feasible_schedules))
            if(len(feasible_schedules)==total_participants):

                for sch in feasible_schedules:
                    slot=sch['slot_id']
                    candidate = sch['candidate_id']
                    slot_current = Slot.objects.get(id=slot)
                    candidate_current = Candidate.objects.get(id=candidate)
                    schedule_current = Schedule.objects.create(slot=slot_current, candidate=candidate_current)
                    print("test")
                    schedule_current.save()
                    messages.success(request, "Success: Interview Scheduled Successfully!")
            


    candidate = Candidate.objects.all()
    schedules = Schedule.objects.all()
    context={
        'candidate':candidate,
        'schedule':schedules
    }
    return render(request, 'schedule.html',context)

