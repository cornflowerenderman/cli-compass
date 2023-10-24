import requests, json, uuid, datetime, sys

args = sys.argv[1:]

from modules.timeConversion import unixToLongChronicleTime
from modules.timeConversion import chronicleTimeToUnix

def getChronicleCategories(urlPrefix,cookies,headers):
    url = urlPrefix+"/Services/ReferenceDataCache.svc/GetAllChronicleCategories?v="+str(uuid.uuid4())+"&page=1&start=0&limit=25"
    r = requests.get(url, headers=headers, cookies=cookies)
    if(r.ok):
        j = json.loads(r.text)
        categories = {}
        for i in j['d']:
            categories[i['id']]=i['name']
        return categories
    else:
        raise Exception(r)

def getChronicleCategoriesStripped(urlPrefix,cookies,headers):
    chronicleCategories = getChronicleCategories(urlPrefix,cookies,headers)
    chronicleCategoriesStripped = []
    for i in chronicleCategories:
        chronicleCategoriesStripped.append(i)
    return chronicleCategoriesStripped

def getChronicleRatings(urlPrefix,cookies,headers):
    url = urlPrefix+"/Services/ReferenceDataCache.svc/GetChronicleRatings?page=1&start=0&limit=25"
    r = requests.get(url, headers=headers, cookies=cookies)
    if(r.ok):
        j = json.loads(r.text)
        categories = {}
        for i in j['d']:
            categories[i['enumValue']]=i['name']
        return categories
    else:
        raise Exception(r)

def writeJson(name,j):
    f = open(name,"w")
    f.write(json.dumps(j))
    f.close()


def getChronicleFeed(urlPrefix,cookies,headers,userId,pageSize,startTime,endTime,staffList):
    chronicleCats = getChronicleCategoriesStripped(urlPrefix,cookies, headers)
    chronicleRatings = getChronicleRatings(urlPrefix,cookies,headers)
    now = datetime.datetime.now()
    unixTimeMillis = int(now.timestamp()*1000)
    url = urlPrefix + "/Services/ChronicleV2.svc/GetUserChronicleFeedThin?sessionstate=readonly&_dc="+str(unixTimeMillis)
    payload = {
        "targetUserId":userId,
        "start":0,
        "pageSize":pageSize,
        "startDate":unixToLongChronicleTime(startTime),
        "endDate":unixToLongChronicleTime(endTime),
        "filterCategoryIds":chronicleCats,
        "asParent":False,
        "page":1,
        "limit":25
    }
    r = requests.post(url,json=payload,cookies=cookies,headers=headers)
    if(r.ok):
        j = json.loads(r.text)['d']
        totalChronicles = j['total']
        chronicleOutput = []
        for i in j['data']:
            chronicle = []
            for a in i['chronicleEntries']:
                temp = {}
                temp['categoryName'] = a['categoryName']
                temp['createdTime'] = chronicleTimeToUnix(a['createdTimestamp'])
                temp['occurredTime'] = chronicleTimeToUnix(a['occurredTimestamp'])
                temp['points'] = a['points']
                if(a['rating'] in chronicleRatings):
                    temp['rating'] = chronicleRatings[a['rating']]
                else:
                    temp['rating']=None
                text = ""
                for j in a['inputFields']:
                    name = j['name']
                    try:
                        value_raw = json.loads(j['value'])
                        value = ""
                        for z in value_raw:
                            if(z['isChecked']):
                                value+="- "+z['valueOption']+": Yes\n"
                    except:
                        value = "- "+j['value']
                    if(value != "- "):
                        text+=name+":\n"
                        text+=value+"\n\n"
                temp['text'] = text.replace("\n\n","\n").replace("\n\n","\n").strip()
                temp['isSickbay'] = a['sickbayEntry']
                temp['templateName'] = a['templateName']
                temp['creator'] = staffList[a['userIdCreator']]
                chronicle.append(temp)
            chronicleOutput.append(chronicle)
        return chronicleOutput
    else:
        raise Exception(r)

