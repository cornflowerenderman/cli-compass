# Centralised request functions, for simplicity and easier debugging

import requests, json

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
                        print("[DEBUG] The server sent an invalid HTTP response")
                        raise requests.exceptions.HTTPError(error)
                except requests.exceptions.SSLError as error:
                    print("[DEBUG] SSL error, check system time and connection")
                    raise requests.exceptions.SSLError(error)
            except (requests.exceptions.ProxyError,requests.exceptions.InvalidProxyURL) as error:
                print("[DEBUG] Proxy error, check proxy settings and try again")
                raise requests.exceptions.ProxyError(error)
        except requests.exceptions.Timeout as error:
            print("[DEBUG] Timed out, check internet connection and proxy settings")
            raise requests.exceptions.Timeout(error)
    except requests.ConnectionError as error:
        print("[DEBUG] Connection error, check internet connection, DNS and proxy settings")
        raise requests.ConnectionError(error)
    if(r.ok):
        if(isJson):
            try:
                return json.loads(r.text)
            except json.decoder.JSONDecodeError as error:
                print("[DEBUG] Error parsing JSON:")
                print(r.text)
                raise json.decoder.JSONDecodeError(error)
        else:
            return r
    else:
        if(r.status_code == 500): #Likely expired/invalid ASP.NET_SessionId cookie
            print("[DEBUG] Server sent HTTP Error 500, check ASP.NET_SessionId cookie")
            raise requests.exceptions.HTTPError("HTTP Response 500")
        elif(r.status_code == 403): #Likely bot detection, check User-Agent
            print("[DEBUG] Server sent HTTP Error 403, likely Anti-bot detection, check User-Agent")
            raise requests.exceptions.HTTPError("HTTP Response 403")
        else: #Unknown response
            print("[DEBUG] Server sent unknown HTTP response ("+str(r.status_code)+")")
            raise requests.exceptions.HTTPError(r)

def doPostRequest(url,cookies,payload):
    return doRequest(True,True,url,cookies,payload)

def doGetRequest(url,cookies):
    return doRequest(False,True,url,cookies,None)
