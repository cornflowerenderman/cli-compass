import requests, json
from modules.timeConversion import convertAttendanceTime
from modules.doRequests import doPostRequest
try:
    import colorama
    from colorama import Fore, Style
except:
    raise Exception("Missing dependency: colorama")

def getAttendance(urlPrefix, cookies, headers, userId):
    j = doPostRequest(urlPrefix+"/services/mobile.svc/GetUserDetails",cookies,{"userId":userId})
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

def printAttendance(attendance):
    print(Fore.LIGHTCYAN_EX+"Today's attendance:"+Style.RESET_ALL)
    if(len(attendance)>0):
        temp = []
        for i in attendance:
            status = i['status']['name']
            if(status=='Present'):
                status=Fore.LIGHTGREEN_EX+Style.BRIGHT+status+Style.RESET_ALL
            elif(status=='Wellbeing' or status=='Gen Edu' or status=='Study' or status=='Excursion'):
                status=Fore.LIGHTBLUE_EX+Style.BRIGHT+status+Style.RESET_ALL
            elif(status!='Not Marked'):
                status=Fore.LIGHTRED_EX+Style.BRIGHT+status+Style.RESET_ALL
            temp.append(status)
        print("  "+(" - ".join(temp)))
    else:
        print("  [No roll]")
    print()
