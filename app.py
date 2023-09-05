#app.py
import argparse
import RPi.GPIO as GPIO
import bme280
import requests
from time import time, ctime
from fan import Fan
from os import system
from ubi import UBI_url, TS_url, IFTTT_ON_url, IFTTT_OFF_url

T = time()
f = Fan()

parser = argparse.ArgumentParser(description='add measure cycle in seconds')
parser.add_argument("--t", default=10, type=int, help="set the time in seconds - default 10")
parser.add_argument("--rH", default=60, type=int, help="relative humidity[rH] level for starting fan")
args=parser.parse_args()

Tcycle = args.t
rHlimit = args.rH

url = TS_url
#url = UBI_url

try:
    #entry state to do measure at start
    t,p,rH = bme280.readBME280All()
    print("Reading @ {3}: {0:3.2f}gC, {1:4.0f}hPa, {2:2.1f}rH   ".format(t, p, rH, ctime())) 
    try:
        #r = requests.post(UBI_url, {'Temperature': t, 'Pressure': p, 'Humidity':rH} )
        r = requests.post(TS_url, {'field1': t, 'field2': p, 'field3':rH} )
    except:
        print("Initial run - some error uccurred during POST data to ubidots" + str(r.status_code) + r.text )
        
    if rH > rHlimit:
        f.FanOn()
        print("Fan on")
        try:
            r = requests.post( IFTTT_ON_url, {'value1': '1', 'value2': '2', 'value3': '3'} )
        except:
            print("IFTTT_ON failed " + str(r.status_code) + r.text)
    else:
        f.FanOff()
        print("Fan Off")
        try:
            r = requests.post( IFTTT_OFF_url, {'T': t, 'P': p, 'H': rH} )
        except:
            print("IFTTT_OFF failed" + r.text)

    #entering endless loop for continous runtime
    while(True):
        if (time()-T) >= Tcycle:     #T in seconds
            
            T = time()
            t,p,rH = bme280.readBME280All()
            system('clear')
            #print("Reading {3}: {0:3.2f}gC, {1:4.0f}hPa, {2:2.1f}rH   ".format(t, p, rH, round(T)))
            print("Reading @ {3}: {0:3.2f}gC, {1:4.0f}hPa, {2:2.1f}rH   ".format(t, p, rH, ctime())) 
            try:
                #r = requests.post(UBI_url, {'Temperature': t, 'Pressure': p, 'Humidity':rH} )
                r = requests.post(TS_url, {'field1': t, 'field2': p, 'field3':rH} )
            except:
                print("Loop run -some error eccurred during data POST. #" + str(r.status_code) + r.text )
            
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

            



