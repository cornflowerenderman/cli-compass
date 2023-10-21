import requests, json
from modules.timeConversion import convertAttendanceTime

def getAttendance(urlPrefix, cookies, headers, userId):
    r = requests.post(urlPrefix+"/services/mobile.svc/GetUserDetails",json={"userId":userId},cookies=cookies,headers=headers)
    if(r.ok):
        j = json.loads(r.text)
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
    else:
        raise Exception(r)
