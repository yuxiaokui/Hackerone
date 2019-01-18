print('''Hackone Fuzzing''')

from lib.fuzz import *
from lib.geturls import *
import threading
import queue
import time

history = []
queuelist = queue.Queue(10000)
queuescan = queue.Queue(10000)


for line in open("./domains.lst"):
    line = line.strip()
    try:
        for url in getUrls(line):
            if url not in history:
                history.append(url)
                queuelist.put(url)
                
    except Exception as e:
        pass

class Produce(threading.Thread):
    def __init__(self):
        super(Produce,self).__init__()
        pass

    def run(self):
        while True: 
            if not queuescan.full():
                url = queuelist.get()
                for i in getUrls(url):
                    print(i)
                    if i not in history:
                        history.append(i)
                        queuelist.put(i)
                        queuescan.put(i)



class Consume(threading.Thread):
    def __init__(self):
        super(Consume,self).__init__()


    def run(self):
        while True:
            #print('list',queuelist.qsize())
            #print('scan',queuescan.qsize())
            if not queuescan.empty():
                url = queuescan.get()
                try:
                    fuzz(url)
                except Exception as e:
                    print(e)



if __name__ == "__main__":
    
    for server_num in range(0, 10):
        server = Produce()
        server.start()

    for customer_num in range(0, 50):
        customer = Consume()
        customer.start()
        
