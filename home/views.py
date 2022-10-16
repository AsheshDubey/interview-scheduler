from datetime import datetime
import imp
import json
from time import strftime
from tracemalloc import start
from django.shortcuts import render
from .models import Candidate, Slot, Schedule
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.contrib import messages
from datetime import datetime as dt
from django.core.mail import send_mail
from django.conf import settings


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

def schedule(request):

    if request.method =='POST':


        body = process_query(str(request.body.decode()))
        participants = body.get("test")
        interview_date = request.POST.get("date")
        start_time = request.POST.get("start-time")
        end_time = request.POST.get("end-time")
        
        current_date = dt.now().date()
        current_time = dt.now().strftime('%H:%M')
        date_selected = dt.strptime(interview_date,'%Y-%m-%d').date()
        time_selected = dt.strptime(start_time, '%H:%M').time().strftime('%H:%M')

        if(end_time>start_time and date_selected>=current_date or time_selected>=current_time):
            
            print("good")
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
                                match_time = match_date.filter(slot__start_time__gte=end_time) | match_date.filter(slot__end_time__lte=start_time)
                                print(len(match_time))
                                if(len(match_time)>0):
                                    try:
                                        slot_new = Slot.objects.get(interview_date=interview_date, start_time=start_time, end_time=end_time)
                                    except:
                                        slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
                                        slot_new.save()
                        
                                    current_paritcipant = Candidate.objects.get(id=participants[0])
                                    schedule_current = Schedule.objects.create(slot=slot_new, candidate=current_paritcipant)
                                    schedule_current.save()
                                    subject='Your Interview has been Scheduled'
                                    message = 'Dear '+str(current_paritcipant.name)+'\n\nYour Interview has been Scheduled for '+slot_new.interview_date.strftime("%d %b, %Y")+' from '+slot_new.start_time.strftime("%H:%M")+' to '+slot_new.end_time.strftime("%H:%M")+'.\nAll The Best'
                                    send_mail(
                                        subject,
                                        message,
                                        settings.EMAIL_HOST_USER,
                                        [current_paritcipant.email],
                                        fail_silently=False
                                    )
                                    print(current_paritcipant.email,"1")
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
                                subject='Your Interview has been Scheduled'
                                message = 'Dear '+str(current_paritcipant.name)+'\n\nYour Interview has been Scheduled for '+slot_new.interview_date.strftime("%d %b, %Y")+' from '+slot_new.start_time.strftime("%H:%M")+' to '+slot_new.end_time.strftime("%H:%M")+'.\nAll The Best'
                                send_mail(
                                    subject,
                                    message,
                                    settings.EMAIL_HOST_USER,
                                    [current_paritcipant.email],
                                    fail_silently=False
                                )
                                print(current_paritcipant.email,"2")
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
                                subject='Your Interview has been Scheduled'
                                message = 'Dear '+str(current_paritcipant.name)+'\n\nYour Interview has been Scheduled for '+slot_new.interview_date.strftime("%d %b, %Y")+' from '+slot_new.start_time.strftime("%H:%M")+' to '+slot_new.end_time.strftime("%H:%M")+'.\nAll The Best'
                                send_mail(
                                    subject,
                                    message,
                                    settings.EMAIL_HOST_USER,
                                    [current_paritcipant.email],
                                    fail_silently=False
                                )
                                print(current_paritcipant.email,"3")
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
                        
                            match_time = match_date.filter(slot__start_time__gte=end_time) | match_date.filter(slot__end_time__lte=start_time)
                            print(len(match_time))
                            if(len(match_time)>0):
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
                    messages.success(request, "Success: Interview Scheduled Successfully!")
                    for sch in feasible_schedules:
                        slot=sch['slot_id']
                        candidate = sch['candidate_id']
                        slot_current = Slot.objects.get(id=slot)
                        candidate_current = Candidate.objects.get(id=candidate)
                        schedule_current = Schedule.objects.create(slot=slot_current, candidate=candidate_current)
                        print("test")
                        schedule_current.save()
                        subject='Your Interview has been Scheduled'
                        message = 'Dear '+str(candidate_current.name)+'\n\nYour Interview has been Scheduled for '+slot_current.interview_date.strftime("%d %b, %Y")+' from '+slot_current.start_time.strftime("%H:%M")+' to '+slot_current.end_time.strftime("%H:%M")+'.\nAll The Best'
                        send_mail(
                            subject,
                            message,
                            settings.EMAIL_HOST_USER,
                            [candidate_current.email],
                            fail_silently=False
                        )
                        print(candidate_current.email,"4")
        else:
            messages.error(request, "Error: Please Pick a Valid Slot!")
                    
            


    candidate = Candidate.objects.all()
    schedules = Schedule.objects.all()
    context={
        'candidate':candidate,
        'schedule':schedules
    }
    return render(request, 'schedule.html',context)

