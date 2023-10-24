#!/bin/python3

import sys, requests, datetime, json

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
from modules.getChronicles import getChronicleFeed

try:
    from colorama import Fore, Style
except:
    raise Exception("Missing dependency: colorama")

args = sys.argv[1:] #Command line switches

if ("--help" in args or "-h" in args or "-" in args or "-?" in args or "/?" in args):
    help = """
    Usage:
      python3 getSchedule.py [options]

    Options:
      --help:                 Shows help page
      --show-learning-tasks:  Shows learning tasks (not implemented, time expensive)
      --show-chronicles:      Shows chronicles (partially implemented, also requires --i-know-what-im-doing)
      --chronicle-max n:      Sets max chronicle entries (don't set stupid values! Keep between 1-25)
      --show-events:          Shows events (not implemented)
      --nerd:                 Shows extra information that is useless to the average user
      --no-schedule:          Disables schedule
      --no-attendance:        Disables attendance
      --no-auth-test:         Disables testing if valid login (not recommended)
      --i-know-what-im-doing  Makes sure you know what you're doing (Features in development)
      --show-news:            Enables news (semi time expensive)
      --news-max n:           Sets max news entries (can sometimes increase speed)
      --no-fancy-links:       Disables web-style links (Use if not supported by your terminal)
      --no-net-test:          Disables checking for an internet connection
    """
    print(help)
    sys.exit()

config = getConfig()
cookies = config['cookies']
headers = config['headers']

urlPrefix = "https://"+config['school']+".compass.education"

if("--no-net-test" not in args):
    timeout = 1
    try:
        requests.head(urlPrefix, headers=headers, timeout=timeout)
    except requests.ConnectionError:
        try:
            requests.head("www.google.com", timeout=timeout)
            print("Connected to www.google.com, compass may be down")
        except requests.ConnectionError:
            print("Could not connect to www.google.com or compass, check your internet connection and try again")
        sys.exit()

print(Fore.LIGHTMAGENTA_EX+"Unofficial CLI Compass Education Client (https://github.com/cornflowerenderman/cli-compass)"+Style.RESET_ALL)
print(Style.BRIGHT+Fore.LIGHTRED_EX+"This version is probably buggy! Use at your own risk!")
print("We will not be responsible for any issues that may arise from using this client!")
print(Style.RESET_ALL)

if("--no-auth-test" not in args):
    valid = testAuth(urlPrefix,cookies,headers)
    if(valid==False):
        raise Exception("Could not authenticate! Fix config.json or log in on browser")

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

if("--show-news" in args):
    maxEntries = -1
    if("--news-max" in args):
        try:
            maxEntries = int(args[args[:-1].index('--news-max')+1])
        except:
            pass
    newsEntries = getAllNews(urlPrefix, cookies, headers, maxEntries)
    printNews(newsEntries)



def getStaffList(urlPrefix,cookies,headers):
    now = datetime.datetime.now()
    unixTimeMillis = int(now.timestamp()*1000)
    url = urlPrefix + "/Services/User.svc/GetAllStaff?sessionstate=readonly&_dc="+str(unixTimeMillis)
    payload = {"page":1,"start":0,"limit":25}
    r = requests.post(url,json=payload,cookies=cookies,headers=headers)
    if(r.ok):
        j = json.loads(r.text)
        output = {}        
        for i in j['d']:
            output[i['id']] = {
                "name":i['n'],
                "username":i['u'],
                "photoId":i['pv'],
                "startDate":i['start'],
                "displayCode":i['displayCode']
            }
        return output
    else:
        raise Exception(r)

if(("--show-chronicles" in args) and ("--i-know-what-im-doing" in args)):
    maxChronicles = 5
    if('--chronicle-max' in args):
        try:
            maxChronicles = int(args[args[:-1].index('--chronicle-max')+1])
        except:
            pass
    start = datetime.datetime(2023,1,1).timestamp()
    end = datetime.datetime(2023,12,31).timestamp()
    staffList=getStaffList(urlPrefix,cookies,headers)
    chronicleFeed = getChronicleFeed(urlPrefix,cookies,headers,userId,maxChronicles,start,end,staffList)
    for a in chronicleFeed:
        for i in a:
            if(i['rating'] == 'Green'):
                print(Fore.LIGHTGREEN_EX,end='')
            elif(i['rating'] == 'Amber'):
                print(Fore.LIGHTYELLOW_EX,end='')
            elif(i['rating'] == 'Red'):
                print(Fore.LIGHTRED_EX,end='')
            elif(i['rating'] == 'Grey'):
                print(Style.DIM,end='')
            print(i["templateName"])
            print("Recorded by "+i['creator']['name'])
            print(i['text'])
            print(i['categoryName'])
            createdTime = datetime.datetime.fromtimestamp(i['createdTime']).strftime('%b %d %H:%M')
            occurredTime = datetime.datetime.fromtimestamp(i['occurredTime']).strftime('%b %d %H:%M')
            print("Recorded "+createdTime+", Occured "+occurredTime)
            print("~~~~~"+Style.RESET_ALL)
        print()
