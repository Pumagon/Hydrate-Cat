#!/usr/bin/env python3

import time

import subprocess, sys, time, kintone, iotutils
from iotutils import getCurrentTimeStamp

import RPi.GPIO as GPIO
from hx711 import HX711
import adafruitSSD1306

from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

interval = 60 
#interval = 5

# kintone setup
sdomain = "karube"
appId = "18"
token = "XXXXXXXXXXXXXXXXXX"

# SSD1306 (OLED) setup
font = ImageFont.truetype('SourceHanSansJP-Medium.otf', 16)
disp = adafruitSSD1306.initialize_display()
image, draw = adafruitSSD1306.initialize_image(disp)

# Show warning message during startup
adafruitSSD1306.write_image(disp, draw, image, font, "** Not Ready **", "Don't put", "Anything.")

try:
    GPIO.setmode(GPIO.BCM)

    # HX711 (scale) setup
    hx = HX711(dout_pin=5, pd_sck_pin=6)
    err = hx.zero()
    if err:
        adafruitSSD1306.write_image(disp, draw, image, font, "", "Tare is unsuccessful.", "")
        raise ValueError('Tare is unsuccessful.')

    # Adjusting scale ratio
    #hx.set_scale_ratio(442.15296367112813)
    hx.set_scale_ratio(442.7005649717514)

    weights = []
    
    while True:
        # reading weight
        reading = round(float(hx.get_weight_mean(20)), 2)

        if reading == 0:
            print("Reading value is 0. Meansuring again.")
            continue

        myMessage = ""

        if len(weights) < 6:
            weights.append(reading)
        elif len(weights) == 6:
            del weights[0]
            weights.append(reading)
            if (sum(weights[3:5]) - sum(weights[0:2])) > 10:
               myMessage = "Cat Hydrated!"

        # Uploading Data to kintone
        date = getCurrentTimeStamp()
        number = reading
        payload = {"app": appId,
                   "record": {"number": {"value": number },
                              "date": {"value": date },
                              "text": {"value": myMessage} }}

        recordId = kintone.uploadRecord(subDomain=sdomain,
                                        apiToken=token,
                                        record=payload)
        if recordId is None:
            sys.exit()

        print(reading, 'g')
        adafruitSSD1306.write_image(disp, draw, image, font, "", str(reading) + " gram", "")
        time.sleep(interval)

except (KeyboardInterrupt, SystemExit):
    adafruitSSD1306.write_image(disp, draw, image, font, "", "Bye", "")
    print('Bye :)')

finally:
    GPIO.cleanup()

