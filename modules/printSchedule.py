from colorama import Fore, Style

from modules.timeConversion import unixToShortTime

def printSchedule(urlPrefix, schedule):
    if(len(schedule)>0):
        widest = 1
        for i in schedule:
            if("info" in i): #These annoying non-standard events
                if(len(i['info'])>widest):
                    widest = len(i['info'])
        teacherWidth = max(widest-17,4)
        schedule[4]['rollMarked'] = False
        for i in schedule:
            start = unixToShortTime(i['start'])
            url = urlPrefix+"/Organise/Activities/Activity.aspx#session/"+i['id'] #Convert sessionId to clickable URL
            startLetter = '# ' if i['type']==1 else '  '
            if("info" in i):
                info = i['info']
                stuff = [start,info,url]
                print((startLetter+'{:8} | {:'+str(widest)+'} | {:>4}').format(*stuff))
            else:
                stuff = [start,i['class'],i['location'],i['teacher'],url]
                entryColour = Fore.LIGHTCYAN_EX if i['rollMarked'] else Fore.LIGHTYELLOW_EX
                print(entryColour+(startLetter+'{:8} | {:8} - {:3} - {:'+str(teacherWidth)+'} | {:>4}').format(*stuff)+Style.RESET_ALL)
    else:
        print("  [Nothing]")
