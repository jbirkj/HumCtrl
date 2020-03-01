# HumCtrl

## source for Raspberry Pi to measure humidity and control a fan accordingly.

### Hardware:
* Raspberry Pi 3 B+
* BME280 sensor board 
* SSR relay (Fotex SSR DA25 )

### Using REST
execution have two optional arguments
Argument "--t" setting the cycle time in seconds for how often to read
Argument "--rH" setting limit of relative humidity for when to start the airflow fan

Example here measure room humidity and temperature every 10 minutes (600seconds) and start fan if relative humidity level is 45 or higher.
``` funciton call example
    python app.py --t=600 --rH=45
```

### Code example
```
    t,p,rH = bme280.readBME280All()
    print("Reading @ {3}: {0:3.2f}gC, {1:4.0f}hPa, {2:2.1f}rH   ".format(t, p, rH, ctime())) 
    r = requests.post(UBI_url, {'Temperature': t, 'Pressure': p, 'Humidity':rH} )

    if rH > rHlimit:
        f.FanOn()
        print("Fan on")
    else:
        f.FanOff()
        print("Fan Off")
```

## References:

Cmd-line args - https://levelup.gitconnected.com/the-easy-guide-to-python-command-line-arguments-96b4607baea1

Clear screen - https://www.geeksforgeeks.org/clear-screen-python/

print-.format - https://www.geeksforgeeks.org/python-output-formatting/

BME280 - https://www.raspberrypi-spy.co.uk/2016/07/using-bme280-i2c-temperature-pressure-sensor-in-python/
code - https://bitbucket.org/MattHawkinsUK/rpispy-misc/raw/master/python/bme280.py

Fotek SSR 25DA - https://easyeda.com/marpik/Fotek_SSR_25DA-2cd47362592f46139ae9a9c5a5eaba19

README.md formatting - https://github.com/adam-p/markdown-here/wiki/Markdown-Cheatsheet

UBIDots example - https://help.ubidots.com/en/articles/1077054-diy-raspberry-pi-temperature-system-with-ubidots

