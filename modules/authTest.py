import requests, json

def testAuth(urlPrefix,cookies,headers):
    if(len(cookies['ASP.NET_SessionId'])!=36): #User has not set valid UUID
        return False
    r = requests.post(urlPrefix+"/services/mobile.svc/TestAuth",json="",cookies=cookies,headers=headers)
    if(r.ok):
        return json.loads(r.text)['d']['success']
    else:
        if(r.status_code == 500): #Likely expired/invalid ASP.NET_SessionId cookie
            return False
        elif(r.status_code == 403): #Likely bot detection, check User-Agent
            return False
        else: #Unknown response
            raise Exception(r)
