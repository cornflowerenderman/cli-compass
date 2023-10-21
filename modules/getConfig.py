import json
try:
    import browser_cookie3
except:
    raise Exception("Missing browser-cookie3 dependency")

#This is a reasonably generic User-Agent that doesn't instantly set off anti-bot detection
#The default of python-requests/2.25.1 results in 403 (forbidden) errors
userAgent = "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"

def getCookieFromBrowser(school):
    try:
        cookiejar = browser_cookie3.load(domain_name=school+".compass.education") #Get browser cookie jar
        cookies = {}
        for i in cookiejar:
            if(i.name == "ASP.NET_SessionId"): #Magic cookie
                cookies[i.name] = i.value
        if(cookies=={}): #Didn't find cookie
            return None
        return cookies
    except:
        return None

def askSchoolName():
    print("School name not found!")
    print("Hint: this is the start of the url")
    for i in range(3):
        school = input("Enter school name: ")
        if("://" in school): #Url pasted
            school = school.split("://")[1]
        if("." in school): #Url pasted
            school = school.split(".")[0]
        if(len(school)>0):
            print("Is this correct? https://"+school+".compass.education/")
            ans = input("Y for yes, any other key for no: ").upper()
            if(ans=='Y'):
                return school
        else:
            print("You did not enter a valid school name or url")
    raise Exception("User isn't following simple instructions")
    
def updateConfig(config): #Overwrites config with new values
    f = open("config.json","w")
    f.write(json.dumps(config))
    f.close()


def getConfig(): #This function is a bit of a mess
    #First look for config.json in current folder, then parent
    config = {}
    try:
        config = json.loads(open("config.json","r").read())
    except:
        try:
            config = json.loads(open("../config.json","r").read())
        except:
            #Config doesn't exist or is invalid
            school = askSchoolName()
            headers = {"User-Agent":userAgent}
            cookies = getCookieFromBrowser(school)
            if(cookies == None):
                raise Exception("Could not find any cookies")
            config=  {"cookies":cookies,"headers":headers,"school":school}
            updateConfig(config)
            return config
    if(config=={}):
        raise Exception("config is blank")
    if("school" not in config):
        config['school']=askSchoolName()
    if(len(config['school'])<1):
        config['school']=askSchoolName()
    if("headers" not in config):
        config['headers'] = {"User-Agent":userAgent}
    if("cookies" not in config):
        config['cookies'] = getCookieFromBrowser(config['school'])
        if(config['cookies']==None):
            raise Exception("Could not find any cookies")
    if(config['cookies']=={} or config['cookies']==None):
        config['cookies'] = getCookieFromBrowser(config['school'])
        if(config['cookies']==None):
            raise Exception("Could not find any cookies")
    if(len(config['cookies']['ASP.NET_SessionId'])!=36):
        config['cookies'] = getCookieFromBrowser(config['school'])
        if(config['cookies']==None):
            raise Exception("Could not find any cookies")
    updateConfig(config)
    return config

