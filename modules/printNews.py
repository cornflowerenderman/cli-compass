from colorama import Fore, Style
from modules.timeConversion import unixToTime
from modules.printLink import getFancyLink

import sys
args = sys.argv[1:]

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
    
