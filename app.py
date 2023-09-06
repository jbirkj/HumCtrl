#app.py
import argparse
import SHT35
import requests
from time import time, ctime
from os import system
from ubi import TS_url

T = time()

parser = argparse.ArgumentParser(description='add measure cycle in seconds')
parser.add_argument("--t", default=10, type=int, help="set the time in seconds - default 10")
args=parser.parse_args()

Tcycle = args.t

try:
    #entry state to do measure at start
    t,rH = SHT35.readSHT35()
    p=0
    print("Reading @ {3}: {0:3.2f}gC, {1:4.0f}hPa, {2:2.1f}rH   ".format(t, p, rH, ctime())) 
    try:
        r = requests.post(TS_url, {'field4': rH} )

    except:
        print("some error uccurred during POST data to ubidots")
        
#entering endless loop for continous runtime
    
    while(True):
        if (time()-T) >= Tcycle:     #T in seconds
            
            T = time()
            t, rH = SHT35.readSHT35()
            p=0
            system('clear')
            print("Reading @ {3}: {0:3.2f}gC, {1:4.0f}hPa, {2:2.1f}rH   ".format(t, p, rH, ctime())) 
            try:
                r = requests.post(TS_url, {'field4': rH} )

            except:
                print("some error eccurred during data POST to UBIduts")

except KeyboardInterrupt:
    print("KB interrupt!")
    
except Exception as e:
    print("Other exception occurred")
    #print(e.message)
    print(e)
    

            



