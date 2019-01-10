print('''Hackone Fuzzing''')

from lib.fuzz import *
from lib.geturls import *

history = []

for line in open("./domains.lst"):
    line = line.strip()
    try:
        for url in getUrls(line):
            if url not in history:
                history.append(url)
                print(url)
                fuzz(url)
    except Exception as e:
        pass
