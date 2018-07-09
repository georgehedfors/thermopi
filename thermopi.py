#!/usr/bin/env python3

import board
import busio
import digitalio
import adafruit_max31855

temp1 = board.D5  # BBQ
temp2 = board.D19 # Meat

spi0 = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
spi1 = busio.SPI(board.SCK, MOSI=board.MOSI, MISO=board.MISO)
cs0 = digitalio.DigitalInOut(temp1)
cs1 = digitalio.DigitalInOut(temp2)
max318551 = adafruit_max31855.MAX31855(spi0, cs0)
max318552 = adafruit_max31855.MAX31855(spi1, cs1)

def get_temp():
    return (max318551.temperature, max318552.temperature+1)
