#!/usr/bin/env python
# coding:utf-8
import spidev
import time
 
# SPI通信を行うための準備 
spi = spidev.SpiDev() #SPI通信を行うオブジェクトを取得
spi.open(0, 0) #通信を開始
spi.max_speed_hz =1000000 #debianのバージョンが9.1の場合は必要
 
# 連続して値を読む
while True:
    try:
        # SPIで値を読む 
        res = spi.xfer2([0x06,0x00,0x00])
        value = ((res[1] & 0x0f) << 8) | res[2]
        print value
        time.sleep(1)
    except KeyboardInterrupt:
        break
 
# 通信を終了する
spi.close()