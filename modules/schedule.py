import json, requests, datetime, sys
from modules.timeConversion import convertScheduleTime, unixToShortTime
from modules.doRequests import doPostRequest
from colorama import Fore, Style
from modules.printLink import getFancyLink

args = sys.argv[1:]

def getSchedule(urlPrefix, cookies, headers, date, userId): #Accepts a datetime date and your UserID
    payload = {
        "date":date.strftime("%Y/%m/%d %I:%M %p"),
        "userId": userId
    }
    j = doPostRequest(urlPrefix+"/services/mobile.svc/GetScheduleLinesForDate",cookies,payload)
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

def printSchedule(urlPrefix, date, schedule):
    today = datetime.date.today()
    if(date==today):
        print(Fore.LIGHTCYAN_EX+"Today's schedule:"+Style.RESET_ALL)
    else:
        print(Fore.LIGHTCYAN_EX+date.strftime("%A")+"'s schedule:"+Style.RESET_ALL)
    if(len(schedule)>0):
        widest = 1
        for i in schedule:
            if("info" in i): #These annoying non-standard events
                if(len(i['info'])>widest):
                    widest = len(i['info'])
        teacherWidth = max(widest-17,4)
        schedule[4]['rollMarked'] = False
        for i in schedule:
            start = unixToShortTime(i['start'])
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
