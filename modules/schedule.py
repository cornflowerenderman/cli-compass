import json, requests, datetime, sys
from modules.timeConversion import convertScheduleTime, unixToShortTime
from modules.doRequests import doPostRequest
from colorama import Fore, Style
from modules.printLink import getFancyLink

args = sys.argv[1:]

def getSchedule(urlPrefix, cookies, headers, startDate, endDate, userId): #Accepts a datetime date and your UserID
    payload = {
        "start": startDate.strftime("%Y-%m-%d"),
        "finish": endDate.strftime("%Y-%m-%d"),
        "userId": userId,
        "homePage": True,
        "isCalendar": True
    }
    j = doPostRequest(urlPrefix+"/services/mobile.svc/GetCalendarEventsByUser",cookies,payload)
    success = j['d']['success']
    if(success):
        rawSchedule = j['d']['data']
        schedule = []
        for i in rawSchedule:
            entry = {}
            entry["start"]=convertScheduleTime(i["startDateTime"])
            entry["end"]=convertScheduleTime(i["finishDateTime"])
            entry["id"]=i["instanceId"]
            entry["running"]=i["runningStatus"]==1
            entry["rollMarked"]=i["rollMarked"]
            entry["type"]=i["activityType"]
            entry["allDay"]=i["allDay"]
            entry["attendanceMode"]=i["attendanceMode"]
            entry["colour"]=i["backgroundColor"]
            rawInfo = i["bottomTitleLine"].split(" - ")
            if(len(rawInfo)==4):
                entry["class"] = rawInfo[1]
                entry["location"] = rawInfo[2].split(" ")[-1]
                entry["teacher"]=rawInfo[3].split(" ")[-1]
            else:
                if(entry['id']==None):
                    entry["info"]=", ".join(i["bottomTitleLine"].split(", ")[1:]) #Remove name from learning task
                else:
                    entry["info"]=i["bottomTitleLine"]
            schedule.append(entry)
        schedule = sorted(schedule, key=lambda k: k['type'], reverse=True)
        schedule = sorted(schedule, key=lambda k: k['start'], reverse=False)            
        return schedule
    else:
        raise Exception(j['technicalMessage'])

def printSchedule(urlPrefix, schedule):
    today = datetime.date.today()
    tommorrow = today + datetime.timedelta(days=1)
    #today = datetime.datetime(today.year,today.month,today.day,0,0)
    currDay = today
    print(Fore.LIGHTCYAN_EX+"Today's schedule:"+Style.RESET_ALL)
    if(len(schedule)>0):
        widest = 1
        for i in schedule:
            if("info" in i): #These annoying non-standard events
                if(len(i['info'])>widest):
                    widest = len(i['info'])
        teacherWidth = max(widest-17,4)
        schedule[4]['rollMarked'] = False
        for i in schedule:
            schedDate = datetime.datetime.fromtimestamp(i['start'])
            schedDate = datetime.date(schedDate.year,schedDate.month,schedDate.day)
            if(currDay<schedDate):
                print("")
                currDay = schedDate
                if(currDay>tommorrow):
                    print(Fore.LIGHTCYAN_EX+currDay.strftime("%A")+"'s schedule:"+Style.RESET_ALL)
                else:
                    print(Fore.LIGHTCYAN_EX+"Tommorrow's schedule:"+Style.RESET_ALL)
            start = unixToShortTime(i['start'])
            url = None
            if(i['id']==None):
                url = "[Learning task]"
            else:
                url = urlPrefix+"/Organise/Activities/Activity.aspx#session/"+i['id'] #Convert sessionId to clickable URL
                if("--no-fancy-links" not in args):
                    url = "Session ID: "+getFancyLink(i['id'],url)
            startLetter = '# ' if i['type']==1 else '  '
            if("info" in i):
                info = i['info']
                stuff = [start,info,url]
                print((startLetter+'{:8} | {:'+str(widest)+'} | {:>4}').format(*stuff))
            else:
                stuff = [start,i['class'],i['location'],i['teacher'],url]
                entryColour = Fore.LIGHTCYAN_EX if i['rollMarked'] else Fore.LIGHTYELLOW_EX
                print(entryColour+(startLetter+'{:8} | {:8} - {:3} - {:'+str(teacherWidth)+'} | {:>4}').format(*stuff)+Style.RESET_ALL)
    else:
        print("  [Nothing]")
    print()
