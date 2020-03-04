#app.py
import sys
import Adafruit_DHT

import argparse
import requests
from time import time, ctime
from os import system
from ubi import UBI_url

T = time()
f = Fan()

parser = argparse.ArgumentParser(description='add measure cycle in seconds')
parser.add_argument("--t", default=10, type=int, help="set the time in seconds - default 10")
args=parser.parse_args()

Tcycle = args.t

sensor = '2302'
pin = 4


try:
    #entry state to do measure at start
    humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
    print("Reading @ {2}: {0:3.2f}gC, {1:2.1f}rH   ".format(temperature, humidity, ctime())) 
    r = requests.post(UBI_url, {'Temperature': temperature, 'Humidity': humidity} )

    #entering endless loop for continous runtime
    while(True):
        if (time()-T) >= Tcycle:     #T in seconds
            
            T = time()
            humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
            system('clear')
            print("Reading @ {2}: {0:3.2f}gC, {1:2.1f}rH   ".format(temperature, humidity, ctime())) 
            r = requests.post(UBI_url, {'Temperature': temperature, 'Humidity': humidity} )
            
except KeyboardInterrupt:
    print("KB interrupt!")
    
except Exception as e:
    print("Other exception occurred")
    print(e)
    

            



