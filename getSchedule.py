#!/bin/python3
import sys
import datetime

args = sys.argv[1:]
#--nerd enables extra information
#--no-schedule disables schedule
#--no-attendance disables attendance
#--no-auth-test disables testing if valid login (not recommended)
#--no-user-id disables finding user-id (will break stuff)
#--news enables news (semi-expensive)
#--news-max 3 sets max news entries (can sometimes increase speed by reducing required request count)

try:
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
from modules.getNews import getAllNews
from modules.printNews import printNews

config = getConfig()
cookies = config['cookies']
headers = config['headers']

urlPrefix = "https://"+config['school']+".compass.education"

if("--no-auth-test" not in args):
    valid = testAuth(urlPrefix,cookies,headers)
    if(valid==False):
        raise Exception("Could not authenticate! Fix config.json or log in on browser")

userId = None
if("--no-user-id" not in args):
    userInfo = getUserInfo(urlPrefix, cookies, headers)
    userId = userInfo['userId'] #Key piece of information for most requests
    userInfoPrintText = "Logged in as "+userInfo['name']+" ("+userInfo['username']
    if("--nerd" in args):
        userInfoPrintText+=", "+str(userInfo['userId']) #--nerd enables UserID to be shown
    print(Fore.LIGHTMAGENTA_EX+userInfoPrintText+")"+Style.RESET_ALL)
    print()

if("--no-attendance" not in args):
    attendance = getAttendance(urlPrefix, cookies, headers, userId)
    printAttendance(attendance)

if("--no-schedule" not in args):
    today = datetime.date.today()
    schedule = getSchedule(urlPrefix,cookies,headers,today,userId)
    printSchedule(urlPrefix, today, schedule)
    next_day = findNextWeekday(today)
    schedule = getSchedule(urlPrefix,cookies,headers,next_day,userId)
    printSchedule(urlPrefix, next_day, schedule)

if("--news" in args):
    maxEntries = -1
    if("--news-max" in args):
        try:
            maxEntries = int(args[args[:-1].index('--news-max')+1])
        except:
            pass
    newsEntries = getAllNews(urlPrefix, cookies, headers, maxEntries)
    printNews(newsEntries)
