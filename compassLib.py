import requests, json, datetime, pytz

cookies = None
headers = None
urlPrefix = None

def testIfValidSession(urlPrefix,cookies,headers):
    if(len(cookies['ASP.NET_SessionId'])!=36): #User has not set valid UUID
        return False
    r = requests.post(urlPrefix+"/services/mobile.svc/TestAuth",json="",cookies=cookies,headers=headers)
    if(r.ok):
        return json.loads(r.text)['d']['success']
    else:
        if(r.status_code == 500): #Likely expired/invalid ASP.NET_SessionId cookie
            return False
        elif(r.status_code == 403): #Likely bot detection, check User-Agent
            return False
        else: #Unknown response
            raise Exception(r)

def getUserId():
    if(cookies==None):
        raise("Cookies not set")
    r = requests.post(urlPrefix+"/services/mobile.svc/GetMobilePersonalDetails",json="",cookies=cookies,headers=headers)
    if(r.ok):
        j = json.loads(r.text)
        success = j['d']['success']
        if(success):
            name = j['d']['data']['firstName']
            userId = j['d']['data']['userId']
            username = j['d']['data']['username']
            print("Logged in as "+name+" ("+username+", "+str(userId)+")")
            return userId
        else:
            raise Exception(j['technicalMessage'])
    else:
        raise Exception(r)

def convertNewsEntryTime(timestamp):
    d = datetime.datetime.strptime(timestamp, "%d/%m/%Y - %I:%M %p")
    d = d.astimezone(pytz.timezone("UTC"))
    d = datetime.datetime(d.year,d.month,d.day,d.hour,d.minute)
    return int(d.timestamp())

def convertAttendanceTime(timestamp):
    d = datetime.datetime.strptime(timestamp, "%d/%m - %I:%M %p")
    year = datetime.datetime.now().year
    d = datetime.datetime(year, d.month, d.day, d.hour, d.minute)
    return int(d.timestamp())

def convertScheduleTime(timestamp):
    return int(datetime.datetime.strptime(timestamp, "%d/%m/%Y - %I:%M %p").timestamp())

def getSchedule(date, userId):
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

def getAttendance(userId):
    r = requests.post(urlPrefix+"/services/mobile.svc/GetUserDetails",json={"userId":userId},cookies=cookies,headers=headers)
    if(r.ok):
        j = json.loads(r.text)
        success = j['d']['success']
        if(success):
            attendance = j['d']['data']['timeLinePeriods']
            for i in range(len(attendance)):
                start = convertAttendanceTime(attendance[i]['start'])
                end = convertAttendanceTime(attendance[i]['finish'])
                status = {"id":attendance[i]['status'],"name":attendance[i]['statusName']}
                attendance[i] = {"start":start,"end":end,"status":status}
            return attendance
        else:
            raise Exception(j['technicalMessage'])
    else:
        raise Exception(r)
