import json, requests
from modules.timeConversion import convertNewsEntryTime
from bs4 import BeautifulSoup
from modules.doRequests import doPostRequest
from colorama import Fore, Style
from modules.timeConversion import unixToTime
from modules.printLink import getFancyLink
import sys
args = sys.argv[1:]

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
    j = doPostRequest(urlPrefix+"/services/mobile.svc/GetNewsFeedPaged",cookies,{"page":pageNumber})
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

def printNews(newsEntries):
    for i in newsEntries:
        time = unixToTime(i['time'])
        top = time + " - "+Fore.LIGHTCYAN_EX+i['title']+Style.RESET_ALL
        bottom = "Author: "+Fore.LIGHTCYAN_EX+i['author']['name']+Style.RESET_ALL+" - Important: "+str(i['important'])
        print(top)
        content = i['content']
        print(Fore.LIGHTGREEN_EX+content+Style.RESET_ALL)
        if(len(i['attachments'])>0):
            print(Fore.LIGHTYELLOW_EX+"Attachments:")
            if("--no-fancy-links" in args):
                maxAttachmentNameLen = 0
                for a in i['attachments']:
                    maxAttachmentNameLen = max(maxAttachmentNameLen,len(a['name']))
                for a in i['attachments']:                
                    stuff = [a['name'],a['url']]
                    print("  "+('{:'+str(maxAttachmentNameLen)+'} | {:8}').format(*stuff))
            else:
                for a in i['attachments']:
                    print("  "+getFancyLink(a['name'],a['url']))
        print(Style.RESET_ALL+bottom)
        print("")
