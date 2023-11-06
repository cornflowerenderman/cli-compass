# Centralised request functions, for simplicity and easier debugging

import requests, json
from colorama import Fore, Style

headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:109.0) Gecko/20100101 Firefox/118.0"}

timeout = 3

def doRequest(isPost,isJson,url,cookies,payload):
    r = None
    try:
        try:
            try:
                try:
                    try:
                        if(isPost):
                            if(payload==None):
                                r = requests.post(url,cookies=cookies,headers=headers, timeout=timeout)
                            else:
                                r = requests.post(url,cookies=cookies,headers=headers,json=payload, timeout=timeout)
                        else:
                            r = requests.get(url,cookies=cookies,headers=headers, timeout=timeout)
                    except requests.exceptions.HTTPError as error:
                        print(Fore.RED+"[DEBUG] The server sent an invalid HTTP response"+Fore.RESET)
                        raise requests.exceptions.HTTPError(error)
                except requests.exceptions.SSLError as error:
                    print(Fore.RED+"[DEBUG] SSL error, check system time and connection"+Fore.RESET)
                    raise requests.exceptions.SSLError(error)
            except (requests.exceptions.ProxyError,requests.exceptions.InvalidProxyURL) as error:
                print(Fore.RED+"[DEBUG] Proxy error, check proxy settings and try again"+Fore.RESET)
                raise requests.exceptions.ProxyError(error)
        except requests.exceptions.Timeout as error:
            print(Fore.RED+"[DEBUG] Timed out, check internet connection and proxy settings"+Fore.RESET)
            raise requests.exceptions.Timeout(error)
    except requests.ConnectionError as error:
        print(Fore.RED+"[DEBUG] Connection error, check internet connection, DNS and proxy settings"+Fore.RESET)
        raise requests.ConnectionError(error)
    if(r.ok):
        if(isJson):
            try:
                return json.loads(r.text)
            except json.decoder.JSONDecodeError as error:
                print(Fore.RED+"[DEBUG] Error parsing JSON:"+Fore.RESET)
                print(r.text)
                raise json.decoder.JSONDecodeError(error)
        else:
            return r
    else:
        if(r.status_code == 500): #Likely expired/invalid ASP.NET_SessionId cookie
            print(Fore.RED+"[DEBUG] Server sent HTTP Error 500, check ASP.NET_SessionId cookie"+Fore.RESET)
            raise requests.exceptions.HTTPError(Fore.RED+"HTTP Response 500"+Fore.RESET)
        elif(r.status_code == 403): #Likely bot detection, check User-Agent
            print(Fore.RED+"[DEBUG] Server sent HTTP Error 403, likely Anti-bot detection, check User-Agent"+Fore.RESET)
            raise requests.exceptions.HTTPError(Fore.RED+"HTTP Response 403"+Fore.RESET)
        else: #Unknown response
            print(Fore.RED+"[DEBUG] Server sent unknown HTTP response ("+str(r.status_code)+")"+Fore.RESET)
            raise requests.exceptions.HTTPError(r)

def doPostRequest(url,cookies,payload):
    return doRequest(True,True,url,cookies,payload)

def doGetRequest(url,cookies):
    return doRequest(False,True,url,cookies,None)
