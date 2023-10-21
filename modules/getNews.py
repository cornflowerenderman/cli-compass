import requests, json
from modules.timeConversion import convertNewsEntryTime
from bs4 import BeautifulSoup

def filterNewsHTML(raw):
    soup = BeautifulSoup(raw, 'html.parser')
    for i in soup.findAll("a"):
        link = i['href']
        text = i.text
        new = ""
        if(link != text):
            new = text + " "
        new += "[Link: "+link+"]"
        i.string = new
    return soup.text.replace("\xa0"," ")

def getNewsPage(urlPrefix, cookies, headers, pageNumber):
    r = requests.post(urlPrefix+"/services/mobile.svc/GetNewsFeedPaged",json={"page":pageNumber},cookies=cookies,headers=headers)
    if(r.ok):
        j = json.loads(r.text)
        output = {"success":j['d']['success'],"error":None}
        if(j['d']['success']):
            output['hasNext'] = j['d']['hasNext']
            output['news'] = []
            raw_news_list = j['d']['data']
            for i in raw_news_list:
                newsEntry = {}
                newsEntry['title']= i['title']
                newsEntry['time'] = convertNewsEntryTime(i['postDate'])
                newsEntry['important']= i['priority']
                if(i['userImageUrl']=="/Assets/Pix/roll/no_user_pic.jpg"): #Blank placeholder image
                    i['userImageUrl']=None
                elif(i['userImageUrl']!=None):
                    i['userImageUrl']=urlPrefix+i['userImageUrl']
                newsEntry['author']={"name":i['uploader'],"img":i['userImageUrl']}
                newsEntry['content'] = filterNewsHTML(i['contentHtml'])
                attachmentsList = i['attachments']
                filteredAttachments = []
                for a in attachmentsList:
                    attachment = {}
                    attachment['isImage']=a['isImage']
                    attachment['name'] = a['originalFileName']
                    attachment['url'] = urlPrefix+"/Services/FileDownload/FileRequestHandler?FileDownloadType=1&file="+str(a['assetId'])
                    filteredAttachments.append(attachment)
                newsEntry['attachments'] = filteredAttachments
                output['news'].append(newsEntry)
        else:
            output['error'] = j['d']['friendlyMessage']
        return output        
    else:
        if(r.status_code == 403):
            raise Exception("403 Error (Likely cloudflare block)")
        elif(r.status_code == 500):
            raise Exception("500 Error (Likely expired cookie)")
        else:
            raise Exception(r)

def getAllNews(urlPrefix, cookies, headers, maxEntries):
    allNews = []
    nonPriorityCount = 0
    for i in range(5):
        if(nonPriorityCount>=maxEntries and maxEntries>0): #We can garrantee we have the [maxEntries] latest entries
            break
        newsPage = getNewsPage(urlPrefix, cookies, headers,i+1)
        if(newsPage['success']):
            for a in newsPage['news']:
                allNews.append(a)
                if(a['important']==False):
                    nonPriorityCount+=1
            if(newsPage['hasNext']!=True):
                break
        else:
            print(newsPage['error'])
            raise Exception("News entry success!=True")
    allNews = sorted(allNews, key=lambda k: k['time'], reverse=True)
    if(maxEntries>0):
        return allNews[0:maxEntries] #Reduce output to [maxEntries]
    else:
        return allNews

