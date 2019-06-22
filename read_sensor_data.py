#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
# Test Netatmo  class
#
import canary_api as Canary
import time, json
from sys import argv

def main():
    #print("something started")
    canary = Canary.Canary("/home/homeassistant/.homeassistant/scripts/Canary_sensor_read/Canary.conf")
    token_got = canary.getAccessToken()
    
    air_quality = ""
    humidity = ""
    temperature = ""
    read_ok=False
    
    #print(token_got)
    if token_got != "NOK":
        location = canary.getLocations()
        # print(location)
        devices=location[0]["devices"]
        for adevice in devices:
            if adevice["activation_status"] == "activated":
                deviceid = str(adevice["id"])
                devicetype = adevice["device_type"]
                # print(deviceid + ', ' + devicetype)
        if len(deviceid)>3:
            measurements=canary.getMeasurements(deviceid, devicetype)
            #print(measurements)
            for ameasurement in measurements:
                #print(ameasurement)
                if "air_quality" in ameasurement["sensor_type"]:
                    air_quality=ameasurement["value"]
                if "humidity" in ameasurement["sensor_type"]:
                    humidity=ameasurement["value"]
                if "temperature" in ameasurement["sensor_type"]:
                    temperature=ameasurement["value"]
                if len(str(humidity))>2:
                    read_ok = True
    status = json.dumps({'read_ok': read_ok,
                         'temperature': temperature,
                         'humidity': humidity,
                         'air_quality': air_quality}, sort_keys=True, indent=4)
    return status

status=main()
print(status)
