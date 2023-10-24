import requests, json

from modules.doRequests import doPostRequest

def getUserInfo(urlPrefix, cookies, headers):
    if(cookies==None):
        raise("Cookies not set")
    j = doPostRequest(urlPrefix+"/services/mobile.svc/GetMobilePersonalDetails",cookies,"")
    success = j['d']['success']
    if(success):
        name = j['d']['data']['firstName']
        userId = j['d']['data']['userId']
        username = j['d']['data']['username']
        return {"name":name,"username":username,"userId":userId}
    else:
        raise Exception(j['technicalMessage'])
