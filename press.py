#!/usr/bin/env python
# coding:utf-8
import spidev
import time
import subprocess

#spiデバイスオープン
spi = spidev.SpiDev()
spi.open(0, 0)
spi.max_speed_hz = 1000000
try:
    while True:
        res = spi.xfer2([0x06,0x00,0x00])
        value = ((res[1] & 0x0f) << 8) | res[2]
        print value
        time.sleep(1)   #sleep 1sec
except KeyboardInterrupt:
    spi.close()