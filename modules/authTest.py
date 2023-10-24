import requests, json

from modules.doRequests import doPostRequest

def testAuth(urlPrefix,cookies,headers):
    if(len(cookies['ASP.NET_SessionId'])!=36): #User has not set valid UUID
        return False
    return doPostRequest(urlPrefix+"/services/mobile.svc/TestAuth",cookies,"")['d']['success']
