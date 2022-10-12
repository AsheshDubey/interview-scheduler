import imp
import json
from django.shortcuts import render
from django.views.generic import ListView
from .models import Candidate, Slot, Schedule, Participant, Interview
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializer import InterviewSerializer, ParticipantSerializer

def process_query(query):
    ls = query.split("&")
    # print(ls)
    body = {}

    for i in ls:
        l = i.split("=")
        # print(l[0],l[1])
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

# @api_view(["POST"])
def schedule(request):
    # body = json.loads(request.body)
    # if request.method =='POST':
    #     print(request.POST)
    # particiants = Participant.objects.all()

    # context={
    #     'participant':particiants
    # }
    # return render(request, 'schedule.html',context)

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
                        
                            # for participant_id in participants:
                                current_paritcipant = Candidate.objects.get(id=participants[0])
                            ##validations b - c -d
                                schedule_current = Schedule.objects.create(slot=slot_new, candidate=current_paritcipant)
                                schedule_current.save()
                            else:
                                print("this is a no no step d")
                        else:
                            try:
                                slot_new = Slot.objects.get(interview_date=interview_date, start_time=start_time, end_time=end_time)
                            except:
                                slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
                                slot_new.save()
                        
                            # for participant_id in participants:
                            current_paritcipant = Candidate.objects.get(id=participants[0])
                            ##validations b - c -d
                            schedule_current = Schedule.objects.create(slot=slot_new, candidate=current_paritcipant)
                            schedule_current.save()
                    else:
                        print("this is a no no step c")
                        try:
                            slot_new = Slot.objects.get(interview_date=interview_date, start_time=start_time, end_time=end_time)
                        except:
                            slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
                            slot_new.save()
                        
                        for participant_id in participants:
                            current_paritcipant = Candidate.objects.get(id=participant_id)
                            ##validations b - c -d
                            schedule_current = Schedule.objects.create(slot=slot_new, candidate=current_paritcipant)
                            schedule_current.save()
            else:
                print("this is a no no step a")
        else:
            total_participants = len(participants)
            print(total_participants)
            feasible_schedules=[]
            feasible_slots=[]
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
                                #feasible_slots.append(slot_new)

                            # for participant_id in participants:
                            current_paritcipant = Candidate.objects.get(id=participant_id)
                            ##validations b - c -d
                            #schedule_current = Schedule.objects.create(slot__id=slot_new.id, candidate__id=current_paritcipant.id)
                            # schedule_current.save()
                            #feasible_schedules.append(schedule_current)
                            feasible_schedules.append({'slot_id':slot_new.id, 'candidate_id': current_paritcipant.id})
                        else:
                            print("this is a no no step d")
                    else:
                        try:
                            slot_new = Slot.objects.get(interview_date=interview_date, start_time=start_time, end_time=end_time)
                        except:
                            slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
                            slot_new.save()
                            #feasible_slots.append(slot_new)
                        
                        # for participant_id in participants:
                        current_paritcipant = Candidate.objects.get(id=participant_id)
                        ##validations b - c -d
                        #schedule_current = Schedule.objects.create(slot__id=slot_new.id, candidate__id=current_paritcipant.id)
                            # schedule_current.save()
                        #feasible_schedules.append(schedule_current)
                        feasible_schedules.append({'slot_id':slot_new.id, 'candidate_id': current_paritcipant.id})
                else:
                    print("this is a no no step c")
                    try:
                        slot_new = Slot.objects.get(interview_date=interview_date, start_time=start_time, end_time=end_time)
                    except:
                        slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
                        slot_new.save()
                        #feasible_slots.append(slot_new)
                        
                # for participant_id in participants:
                    current_paritcipant = Candidate.objects.get(id=participant_id)
                    ##validations b - c -d
                    feasible_schedules.append({'slot_id':slot_new.id, 'candidate_id': current_paritcipant.id})

                    # schedule_current = Schedule.objects.create(slot__id=slot_new.id, candidate__id=current_paritcipant.id)
                            # schedule_current.save()
                    #feasible_schedules.append(schedule_current)
            print(len(feasible_schedules))
            if(len(feasible_schedules)==total_participants):
                # for slo in feasible_slots:
                #     slo.save()
                for sch in feasible_schedules:
                    slot=sch['slot_id']
                    candidate = sch['candidate_id']
                    slot_current = Slot.objects.get(id=slot)
                    candidate_current = Candidate.objects.get(id=candidate)
                    schedule_current = Schedule.objects.create(slot=slot_current, candidate=candidate_current)
                    print("test")
                    schedule_current.save()
            


        # slot_new = Slot.objects.create(interview_date=interview_date, start_time=start_time, end_time=end_time)
        # slot_new.save()
        # for participant_id in participants:
        #     current_paritcipant = Candidate.objects.get(id=participant_id)
        #     ##validations b - c -d
        #     schedule_current = Schedule.objects.create(slot=slot_new, candidate=current_paritcipant)
        #     schedule_current.save()

    candidate = Candidate.objects.all()
    schedules = Schedule.objects.all()
    context={
        'candidate':candidate,
        'schedule':schedules
    }
    return render(request, 'schedule.html',context)

# @api_view(["DELETE"])
# def deleteInterview(request):
#     body = json.loads(request.body)
#     interview_id = body.get("interview_id")
#     try:
#         interview = Interview.objects.get(id=interview_id)
#     except:
#         return Response({"msg":"no meeting found"})

#     user = interview.user_email
#     date = interview.interview_date
#     interview.delete()

#     try:
#         interviews_remaining = Interview.objects.filter(user_email=user)
    
#         if len(interviews_remaining)==0:
#             user.is_active = False
#             user.save()
#     except:
#         user.is_active = False
#         user.save()
    
#     return Response({"msg":"meeting deleted"})

# @api_view(["POST",'PUT'])
# def edit(request):
#     body = json.loads(request.body)
#     interview_id = body.get("interview_id")
#     try:
#         interview = Interview.objects.get(id=interview_id)
#     except:
#         return Response({"msg":"no meeting found"})
#     #user = Participant.objects.get(id = int(body['user_email']))
#     start_time = body.get("start_time")
#     end_time = body.get("end_time")
#     interview_date = body.get("date")

#     #logic to check conflict

#     #interview.user_email = user
#     ##if valid
#     interview.start_time = start_time
#     interview.end_time = end_time
#     interview.interview_date = interview_date
#     interview.save()

#     ## else do nothing
#     return Response({"msg":"Successful"})
#     return render(request, 'edit.html')


# @api_view(['GET'])
# def allInterviews(req):
#     ls = InterviewSerializer(Interview.objects.all(),many = True).data
#     return Response(ls)

# @api_view(['GET'])
# def allParticipants(req):
#     ls = ParticipantSerializer(Participant.objects.all(),many = True).data
#     return Response(ls)



# @api_view(["POST"])
# def add_new_interview(request):
#     body = json.loads(request.body)
#     user = Participant.objects.get(id = int(body['user_email']))

#     ##logic to check conflict 


#     obj = Interview.objects.create(interview_date = body['interview_date'],start_time=body['start_time']
#                                 ,end_time=body['end_time'],user_email=user)
#     user.is_active=True
#     user.save()
#     obj.save()
#     return Response({"ok":True})

