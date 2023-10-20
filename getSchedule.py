import compassLib

import datetime, colorama, json
from colorama import Fore, Style

def findNextSchoolDay():
    today = datetime.date.today()
    next_day = today + datetime.timedelta(days=1)
    while next_day.weekday() >= 5:
        next_day += datetime.timedelta(days=1)
    return next_day

def printSchedule(date,userId):
    schedule = compassLib.getSchedule(date,userId)
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
    

print(Fore.LIGHTMAGENTA_EX+"CLI Compass (https://github.com/cornflowerenderman/cli-compass)"+Style.RESET_ALL)
print(Style.BRIGHT+Fore.LIGHTRED_EX+"This version is probably buggy! Use at your own risk"+Style.RESET_ALL)

valid = compassLib.testIfValidSession(compassLib.urlPrefix,compassLib.cookies,compassLib.headers)
if(valid==False):
    raise Exception("Could not authenticate! Check config.json")

print(Fore.LIGHTMAGENTA_EX)
userId = compassLib.getUserId()
print(Style.RESET_ALL)

print(Fore.LIGHTCYAN_EX+"Today's attendance:"+Style.RESET_ALL)
attendance = compassLib.getAttendance(userId)
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
tommorrow = findNextSchoolDay()

print(Fore.LIGHTCYAN_EX+"Today's schedule:"+Style.RESET_ALL)
printSchedule(today,userId)
print("")
print(Fore.LIGHTCYAN_EX+"Next school day:"+Style.RESET_ALL)
printSchedule(tommorrow,userId)
print("")
