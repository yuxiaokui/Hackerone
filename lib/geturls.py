import PyChromeDevTools

def getUrls(target):
    chrome = PyChromeDevTools.ChromeInterface(host="60.205.229.131",port=9223)
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
    return result


