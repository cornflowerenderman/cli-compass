import requests, json

def getUserInfo(urlPrefix, cookies, headers):
    if(cookies==None):
        raise("Cookies not set")
    r = requests.post(urlPrefix+"/services/mobile.svc/GetMobilePersonalDetails",json="",cookies=cookies,headers=headers)
    if(r.ok):
        j = json.loads(r.text)
        success = j['d']['success']
        if(success):
            name = j['d']['data']['firstName']
            userId = j['d']['data']['userId']
            username = j['d']['data']['username']
            return {"name":name,"username":username,"userId":userId}
        else:
            raise Exception(j['technicalMessage'])
    else:
        raise Exception(r)

