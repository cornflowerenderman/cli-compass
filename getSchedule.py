#!/bin/python3

try:
    import datetime
    from colorama import Fore, Style
except:
    raise Exception("Missing dependency: colorama")

print(Fore.LIGHTMAGENTA_EX+"Unofficial CLI Compass Education Client (https://github.com/cornflowerenderman/cli-compass)"+Style.RESET_ALL)
print(Style.BRIGHT+Fore.LIGHTRED_EX+"This version is probably buggy! Use at your own risk!")
print("We will not be responsible for any issues that may arise from using this client!")
print(Style.RESET_ALL)

from modules.getConfig import getConfig
from modules.authTest import testAuth
from modules.getAttendance import getAttendance
from modules.getSchedule import getSchedule
from modules.getUserInfo import getUserInfo
from modules.timeConversion import findNextWeekday
from modules.printAttendance import printAttendance
from modules.printSchedule import printSchedule

config = getConfig()
cookies = config['cookies']
headers = config['headers']

urlPrefix = "https://"+config['school']+".compass.education"

valid = testAuth(urlPrefix,cookies,headers)
if(valid==False):
    raise Exception("Could not authenticate! Fix config.json or log in on browser")

userInfo = getUserInfo(urlPrefix, cookies, headers)
userId = userInfo['userId'] #Key piece of information for most requests


print(Fore.LIGHTMAGENTA_EX+"Logged in as "+userInfo['name']+" ("+userInfo['username']+", User ID: "+str(userInfo['userId'])+")"+Style.RESET_ALL)
print()

attendance = getAttendance(urlPrefix, cookies, headers, userId)
printAttendance(attendance)
print()

today = datetime.date.today()
next_day = findNextWeekday(today)

print(Fore.LIGHTCYAN_EX+"Today's schedule:"+Style.RESET_ALL)

schedule = getSchedule(urlPrefix,cookies,headers,today,userId)
printSchedule(urlPrefix, schedule)

print()
print(Fore.LIGHTCYAN_EX+"Next school day:"+Style.RESET_ALL)
schedule = getSchedule(urlPrefix,cookies,headers,next_day,userId)
printSchedule(urlPrefix, schedule)
print()
