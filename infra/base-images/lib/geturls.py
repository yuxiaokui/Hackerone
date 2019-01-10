from bs4 import BeautifulSoup
from urllib.parse import urlparse
import PyChromeDevTools
from urllib.request import urlopen


def getUrls(target):
    '''
    chrome = PyChromeDevTools.ChromeInterface(host="xxx",port=9223)
    chrome.Network.enable()
    chrome.Page.enable()

    chrome.Page.navigate(url = target)
    event,messages=chrome.wait_event("Page.frameStoppedLoading", timeout=10)
    result = []
    for m in messages:
        if "method" in m and m["method"] == "Network.responseReceived":
            try:
                url = m["params"]["response"]["url"]
                result.append(url) 
            except:
                pass
    '''
    result = []

    soup = BeautifulSoup(urlopen(target).read(),'html.parser')
    for item in soup.find_all('a'):
        result.append(item.get("href"))
    
    targetUp = urlparse(target)
    
    data = []
    for url in result:
        if url is None:
            pass
        elif url[0:2] == '//':
            data.append(targetUp.scheme + ":" + url)
        elif url[0:4] == 'http':
            data.append(url)
        else:
            pass

    data = list(set(data))
    return data

#for i in getUrls("http://www.taobao.com/"):
#    print (i)
