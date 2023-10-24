import requests, json
from modules.timeConversion import convertAttendanceTime
from modules.doRequests import doPostRequest

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
