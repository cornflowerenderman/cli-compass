import colorama
from colorama import Fore, Style

print(Fore.LIGHTMAGENTA_EX+"CLI Compass (https://github.com/cornflowerenderman/cli-compass)"+Style.RESET_ALL)
print(Style.BRIGHT+Fore.LIGHTRED_EX+"This version is probably buggy! Use at your own risk"+Style.RESET_ALL)

import compassLib
from modules.getConfig import getConfig

config = getConfig()
compassLib.cookies = config['cookies']
compassLib.headers = config['headers']
school = config['school']

compassLib.urlPrefix = "https://"+school+".compass.education"



import datetime, json

def findNextSchoolDay(day):
    next_day = day + datetime.timedelta(days=1)
    while next_day.weekday() >= 5:
        next_day += datetime.timedelta(days=1)
    return next_day

def printSchedule(date,userId):
    schedule = compassLib.getSchedule(date,userId)
    if(len(schedule)>0):
        widest = 1
        for i in schedule:
            if("info" in i):
                if(len(i['info'])>widest):
                    widest = len(i['info'])
        teacherWidth = max(widest-17,4)
        schedule[4]['rollMarked'] = False
        for i in schedule:
            start = datetime.datetime.fromtimestamp(i['start']).strftime('%I:%M %p')
            url = compassLib.urlPrefix+"/Organise/Activities/Activity.aspx#session/"+i['id']
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

valid = compassLib.testIfValidSession(compassLib.urlPrefix,compassLib.cookies,compassLib.headers)
if(valid==False):
    raise Exception("Could not authenticate! Fix config.json or log in on browser")

print(Fore.LIGHTMAGENTA_EX)
userId = compassLib.getUserId()
print(Style.RESET_ALL)

attendance = compassLib.getAttendance(userId)
if(len(attendance)>0):
    print(Fore.LIGHTCYAN_EX+"Today's attendance:"+Style.RESET_ALL)
    temp = []
    for i in attendance:
        status = i['status']['name']
        if(status=='Present'):
            status=Fore.LIGHTGREEN_EX+Style.BRIGHT+status+Style.RESET_ALL
        elif(status!='Not Marked'):
            status=Fore.LIGHTRED_EX+Style.BRIGHT+status+Style.RESET_ALL
        elif(status=='Wellbeing') or ('Gen Edu'):
            status=Fore.BLUE+Style.BRIGHT+status+Style.RESET_ALL
        temp.append(status)
    print("  "+(" - ".join(temp)))
    print("")


today = datetime.date.today()
tommorrow = findNextSchoolDay(today)

print(Fore.LIGHTCYAN_EX+"Today's schedule:"+Style.RESET_ALL)
printSchedule(today,userId)
print("")
print(Fore.LIGHTCYAN_EX+"Next school day:"+Style.RESET_ALL)
printSchedule(tommorrow,userId)
print("")
