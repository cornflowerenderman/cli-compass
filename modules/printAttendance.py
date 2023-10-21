try:
    import colorama
    from colorama import Fore, Style
except:
    raise Exception("Missing dependency: colorama")

def printAttendance(attendance):
    print(Fore.LIGHTCYAN_EX+"Today's attendance:"+Style.RESET_ALL)
    if(len(attendance)>0):
        temp = []
        for i in attendance:
            status = i['status']['name']
            if(status=='Present'):
                status=Fore.LIGHTGREEN_EX+Style.BRIGHT+status+Style.RESET_ALL
            elif(status!='Not Marked'):
                status=Fore.LIGHTRED_EX+Style.BRIGHT+status+Style.RESET_ALL
            elif(status=='Wellbeing') or ('Gen Edu'):
                status=Fore.BLUE+Style.BRIGHT+status+Style.RESET_ALL
            temp.append(status)
        print("  "+(" - ".join(temp)))
    else:
        print("  [No roll]")
