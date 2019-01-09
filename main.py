print('''Fuck The Web In Hackone!''')

from lib.fuzz import *
from lib.geturls import *

his = []

for line in open("./alibaba/domains.lst"):
    line = line.strip()
    try:
        for url in getUrls(line):
            if url not in his:
                his.append(url)
                fuzz(url)
    except:
        pass
        
    
