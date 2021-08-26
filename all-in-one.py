#!/usr/bin/env python3
import time
from pms5003 import PMS5003, ReadTimeoutError
import logging
from Adafruit_IO import *

logging.basicConfig(
    format=' %(message)s',
    level=logging.INFO,
    datefmt='%Y-%m-%d %H:%M:%S')

logging.info("""particulates.py - Print readings from the PMS5003 particulate sensor.

Press Ctrl+C to exit!

""")
#adafruit IO username and key
ADAFRUIT_IO_USERNAME = 'usrename here'
ADAFRUIT_IO_KEY ='adafruit key here'

aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)



pms5003 = PMS5003()
time.sleep(1.0)




try:
    while True:
        try:
            readings = pms5003.read()
            logging.info(readings)
            #takes reading from pm sensor and casts to a float.
            data_1 = float(readings.pm_ug_per_m3(1.0))          #PM1 ultrafine particles
            data_2_5 = float(readings.pm_ug_per_m3(2.5))        #PM2.5 combustion particles, organic compounds, metals 
            data_10 = float(readings.pm_ug_per_m3(10))          #PM10 dust, pollen, mould spores
            #sends readings to Adafruit feed
            aio.send('particulate-matter.pm1', data_1)
            aio.send('particulate-matter.pm-2-5', data_2_5)
            aio.send('particulate-matter.pm-10', data_10)
            time.sleep(6.0)
            #display pm readings in terminal 
            print([data_1, data_2_5, data_10])
        except ReadTimeoutError:
            pms5003 = PMS5003()
except KeyboardInterrupt:
    pass
