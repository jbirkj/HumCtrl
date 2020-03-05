#app.py
import argparse
import RPi.GPIO as GPIO
import bme280
import requests
from time import time, ctime
from fan import Fan
from os import system
from ubi import UBI_url

T = time()
f = Fan()

parser = argparse.ArgumentParser(description='add measure cycle in seconds')
parser.add_argument("--t", default=10, type=int, help="set the time in seconds - default 10")
parser.add_argument("--rH", default=60, type=int, help="relative humidity[rH] level for starting fan")
args=parser.parse_args()

Tcycle = args.t
rHlimit = args.rH
try:
    #entry state to do measure at start
    t,p,rH = bme280.readBME280All()
    print("Reading @ {3}: {0:3.2f}gC, {1:4.0f}hPa, {2:2.1f}rH   ".format(t, p, rH, ctime())) 
    try:
        r = requests.post(UBI_url, {'Temperature': t, 'Pressure': p, 'Humidity':rH} )
    except:
        print("some error uccurred during POST data to ubidots")
        
    if rH > rHlimit:
        f.FanOn()
        print("Fan on")
    else:
        f.FanOff()
        print("Fan Off")

    #entering endless loop for continous runtime
    while(True):
        if (time()-T) >= Tcycle:     #T in seconds
            
            T = time()
            t,p,rH = bme280.readBME280All()
            system('clear')
            #print("Reading {3}: {0:3.2f}gC, {1:4.0f}hPa, {2:2.1f}rH   ".format(t, p, rH, round(T)))
            print("Reading @ {3}: {0:3.2f}gC, {1:4.0f}hPa, {2:2.1f}rH   ".format(t, p, rH, ctime())) 
            try:
                r = requests.post(UBI_url, {'Temperature': t, 'Pressure': p, 'Humidity':rH} )
            except:
                print("some error eccurred during data POST to UBIduts")
            
            if rH > rHlimit:
                f.FanOn()
                print("Fan on")
            else:
                f.FanOff()
                print("Fan Off")
                
except KeyboardInterrupt:
    print("KB interrupt!")
    
except Exception as e:
    print("Other exception occurred")
    #print(e.message)
    print(e)
    
finally:
    GPIO.cleanup()

            



