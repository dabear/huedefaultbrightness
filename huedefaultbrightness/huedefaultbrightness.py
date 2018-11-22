#!/usr/bin/env python
from __future__ import division
from phue import Bridge
import nightscout
import time
import sys
import datetime
from dateutil.tz import tzlocal
import pytz

MAX_BRIGHTNESS = 254


def get_nowtime():
    zone = tzlocal()
    return datetime.datetime.now().replace(tzinfo=zone)

def set_brightness(lightname, percent):
    light.brightness = int(255*(percent/100))-1 #zero indexeded

def runit(bridge_ip, lightname):
    try:
        b = Bridge(bridge_ip)
        b.connect()
        all_lights = b.get_light_objects('name')
    except Exception as e:
        print("Could not connect to light: {}".format(e.message))
        sys.exit()
    
    try:
        light = all_lights[lightname]

    except KeyError:
        print("Could not find light '{0}', Exiting..".format(lightname))
        sys.exit(-3)
    except:
        print("Could not find hue lights, Exiting...")
        sys.exit(-3)

    lightfile = '/tmp/{}.lightstate'.format(light.name)

    if light.brightness != MAX_BRIGHTNESS:
        print("saving light brightness")
        try:
            with open(lightfile, "w") as f:
                #save last onstate and brightness
                offornot = "on" if light.reachable else "off"
                read_data = f.write("{}|{}".format(offornot, light.brightness))
        except IOError:
            print("could not save state, aborting")
            sys.exit(-1)

        
    elif light.reachable and light.brightness == MAX_BRIGHTNESS:
        print("light is reachable, but has been reset to full brightness, reverting")
        #reset light to last state
        try:
            with open(lightfile, "r") as f:
                contents = f.readline()
                statevals = contents.split("|")
                prevonstate = statevals[0]
                prevbrightness = statevals[1]
        except IOError:
            print("could not read last state, aborting")
            sys.exit(-1)
        except IndexError:
            print("could not read last state correctly, aborting")
            sys.exit(-1)

        if prevbrightness != MAX_BRIGHTNESS:
            print("prevbrightness != MAX_BRIGHTNESS:")
            light.brightness = int(prevbrightness)



    
if __name__ == "__main__":
    bridge_ip = sys.argv[1] #"192.168.1.211"
    lightname = sys.argv[2] #"dialys1"
    
    runit(bridge_ip, lightname)



