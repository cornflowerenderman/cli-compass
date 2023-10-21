#!/bin/python3

import requests, json, datetime     #Built-in libraries

try:
    from modules.getConfig import getConfig
    from modules.authTest import testAuth
    from modules.getAttendance import getAttendance
    from modules.getSchedule import getSchedule
    from modules.getUserInfo import getUserInfo
    from modules.timeConversion import findNextWeekday
except:
    raise Exception("Missing sub-components, try redownloading this project")

try:
    import colorama     #For terminal colouring
    from colorama import Fore, Style
except:
    raise Exception("Missing dependency: colorama")

print(Fore.LIGHTMAGENTA_EX+"Unofficial CLI Compass Education Client (https://github.com/cornflowerenderman/cli-compass)"+Style.RESET_ALL)
print(Style.BRIGHT+Fore.LIGHTRED_EX+"This version is probably buggy! Use at your own risk!")
print("We will not be responsible for any issues that may arise from using this client!"+Style.RESET_ALL)

config = getConfig()
cookies = config['cookies']
headers = config['headers']

urlPrefix = "https://"+config['school']+".compass.education"

def printSchedule(date,userId):
    schedule = getSchedule(urlPrefix,cookies,headers,date,userId)
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
            url = urlPrefix+"/Organise/Activities/Activity.aspx#session/"+i['id']
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

valid = testAuth(urlPrefix,cookies,headers)

if(valid==False):
    raise Exception("Could not authenticate! Fix config.json or log in on browser")

print(Fore.LIGHTMAGENTA_EX)
userInfo = getUserInfo(urlPrefix, cookies, headers)
print("Logged in as "+userInfo['name']+" ("+userInfo['username']+", "+str(userInfo['userId'])+")")
userId = userInfo['userId']
print(Style.RESET_ALL)

attendance = getAttendance(urlPrefix, cookies, headers, userId)
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
tommorrow = findNextWeekday(today)

print(Fore.LIGHTCYAN_EX+"Today's schedule:"+Style.RESET_ALL)
printSchedule(today,userId)
print("")
print(Fore.LIGHTCYAN_EX+"Next school day:"+Style.RESET_ALL)
printSchedule(tommorrow,userId)
print("")
