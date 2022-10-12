import requests
import json

base_url = "http://127.0.0.1:8000/"

def checkUpdate(interview_id):
    data = {
        "interview_id":interview_id,
        "start_time":"12:00:00",
        "end_time":"13:30:00",
        "date":"2022-10-15" ##yyyy-mm-dd
        
    }
    json_data = json.dumps(data)
    print("#####################")
    URL = base_url+'edit'
    headers = {'content-Type':'application/json'}
    r = requests.post(url= URL, headers=headers,data=json_data)
    data=r.json()
    #data = json.loads(data)
    print(data)
def allParticipants():
    
    URL = base_url+'participants'
    #headers = {'content-Type':'application/json'}
    r = requests.get(url= URL)
    data=r.json()
    #data = json.loads(data)
    print(data)
#checkUpdate(2)
allParticipants()