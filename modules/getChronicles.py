import requests, json, uuid, datetime, sys

args = sys.argv[1:]

from modules.timeConversion import unixToLongChronicleTime
from modules.timeConversion import chronicleTimeToUnix

from modules.doRequests import doPostRequest
from modules.doRequests import doGetRequest

def getChronicleCategories(urlPrefix,cookies):
    url = urlPrefix+"/Services/ReferenceDataCache.svc/GetAllChronicleCategories?v="+str(uuid.uuid4())+"&page=1&start=0&limit=25"
    j = doGetRequest(url, cookies)
    categories = {}
    for i in j['d']:
        categories[i['id']]=i['name']
    return categories

def getChronicleCategoriesStripped(urlPrefix,cookies):
    chronicleCategories = getChronicleCategories(urlPrefix,cookies)
    chronicleCategoriesStripped = []
    for i in chronicleCategories:
        chronicleCategoriesStripped.append(i)
    return chronicleCategoriesStripped

def getChronicleRatings(urlPrefix,cookies):
    url = urlPrefix+"/Services/ReferenceDataCache.svc/GetChronicleRatings?page=1&start=0&limit=25"
    j = doGetRequest(url, cookies)
    categories = {}
    for i in j['d']:
        categories[i['enumValue']]=i['name']
    return categories

def writeJson(name,j):
    f = open(name,"w")
    f.write(json.dumps(j))
    f.close()


def getChronicleFeed(urlPrefix,cookies,userId,pageSize,startTime,endTime,staffList):
    chronicleCats = getChronicleCategoriesStripped(urlPrefix,cookies)
    chronicleRatings = getChronicleRatings(urlPrefix,cookies)
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
    j = doPostRequest(url,cookies,payload)['d']
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
                    #TODO: Sickbay chronicles have time in format 2007-12-31T23:17:00.000Z when they should be converted to 10:17 AM
                    value_raw = json.loads(j['value'])
                    try:
                        value = ""
                        for z in value_raw:
                            if(z['isChecked']):
                                value+="- "+z['valueOption']+": Yes\n"
                    except:
                        value="- "
                except:
                    value = "- "+j['value']
                if(value != "- "):
                    text+=name+":\n"
                    text+=value+"\n\n"
            temp['text'] = text.replace("\n\n","\n").replace("\n\n","\n").replace(".:",":").strip()
            temp['isSickbay'] = a['sickbayEntry']
            temp['templateName'] = a['templateName']
            if(a['userIdCreator'] in staffList):
                temp['creator'] = staffList[a['userIdCreator']]
            else:
                temp['creator'] = "[UserID:"+str(a['userIdCreator'])+"]" #Not in staff list
            chronicle.append(temp)
        chronicleOutput.append(chronicle)
    return chronicleOutput

