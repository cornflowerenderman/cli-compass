import json, requests
from modules.timeConversion import convertScheduleTime

def getSchedule(urlPrefix, cookies, headers, date, userId): #Accepts a datetime date and your UserID
    payload = {
        "date":date.strftime("%Y/%m/%d %I:%M %p"),
        "userId": userId
    }
    r = requests.post(urlPrefix+"/services/mobile.svc/GetScheduleLinesForDate",json=payload,headers=headers,cookies=cookies)
    if(r.ok):
        j = json.loads(r.text)
        success = j['d']['success']
        if(success):
            rawSchedule = j['d']['data']
            schedule = []
            for i in rawSchedule:
                entry = {}
                entry["start"]=convertScheduleTime(i["start"])
                entry["end"]=convertScheduleTime(i["finish"])
                entry["id"]=i["instanceId"]
                entry["running"]=i["runningStatus"]==1
                entry["rollMarked"]=i["rollMarked"]
                entry["type"]=i["activityType"]
                entry["allDay"]=i["allDay"]
                entry["attendanceMode"]=i["attendanceMode"]
                entry["colour"]=i["backgroundColor"]
                rawInfo = i["topAndBottomLine"].split(" - ")
                if(len(rawInfo)==5):
                    entry["class"] = rawInfo[2]
                    entry["location"] = rawInfo[3].split(" ")[-1]
                    entry["teacher"]=rawInfo[4].split(" ")[-1]
                else:
                    if(len(rawInfo)>1):
                        entry["info"]=" - ".join(rawInfo[1:])
                    else:
                        entry["info"]=i["topAndBottomLine"]
                schedule.append(entry)
            schedule = sorted(schedule, key=lambda k: k['type'], reverse=True)
            schedule = sorted(schedule, key=lambda k: k['start'], reverse=False)            
            return schedule
        else:
            raise Exception(j['technicalMessage'])
    else:
        raise Exception(r)
