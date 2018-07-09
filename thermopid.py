#!/usr/bin/env python3

import re
import sys
import time
import board
import busio
import digitalio
import subprocess
import adafruit_max31855
import fourletterphat as flp

temp1 = board.D5  # BBQ
temp2 = board.D19 # Meat

spi0 = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
spi1 = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs0 = digitalio.DigitalInOut(temp1)
cs1 = digitalio.DigitalInOut(temp2)
max318551 = adafruit_max31855.MAX31855(spi0, cs0)
max318552 = adafruit_max31855.MAX31855(spi1, cs1)

re_ipaddr = re.compile(r"inet\s([0-9.]+)\/", flags=re.M)

def get_temp():
    return (max318551.temperature, max318552.temperature)

def dprint(s):
    if len(s) > 4:
        s = "   " + s + "    "
        for i in range(len(s)-4):
            flp.print_str(s[i:i+4])
            flp.show()
            time.sleep(0.25)
    else:
        flp.print_str(s)
        flp.show()

    return

if __name__ == "__main__":
    # Welcome message
    dprint("THERMOPI")

    # Check thermometers
    temps = get_temp()
    if temps[0] == 0.0 or temps[1] == 0.0:
        dprint("ETER")
        print("Error reading thermometer (%s / %s)" % temps)
        sys.exit(0)

    dprint("LDNG")

    # Wait for ip on wlan0
    for i in range(10):
        p = subprocess.Popen(["ip", "addr", "show", "wlan0"], stdout=subprocess.PIPE)
        res = p.communicate()[0]
        addr = re_ipaddr.findall(str(res))
        
        if len(addr) > 0:
            break

        time.sleep(1)

    if len(addr) == 0:
        dprint("EWIF")
        print("Error finding wifi address")
        time.sleep(5)

    # Display current address
    dprint(addr[0].replace(".", ","))

    # Thermometer loop
    while True:
        temps = get_temp()

        t = str(int(temps[0]))
        pad = 3-len(t)
        dprint("B" + " " * pad + t)

        time.sleep(5)

        t = str(int(temps[1]))
        pad = 3-len(t)
        dprint("M" + " " * pad + t)

        time.sleep(5)
