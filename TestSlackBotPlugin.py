# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re
import RPi.GPIO as GPIO
import time
import sys
reload(sys)
# デフォルトの文字コードを変更
sys.setdefaultencoding('utf-8')

def setservo():
    GPIO.setmode(GPIO.BCM)

    #GPIO4を制御パルスの出力に設定
    gp_out=4
    GPIO.setup(gp_out, GPIO.OUT)
    servo = GPIO.PWM(gp_out, 50)

    servo.start(0)
    return servo

def lockRead():
    path = u'locklog.txt'
    with open(path) as f:
        l = f.readlines()
    return  l[0].strip()

def lockWrite(lock):
    path = u'locklog.txt'
    with open(path, mode=u'w') as f:
        f.write(lock)

def doOpenKeyOrder():
        servo = setservo()
        servo.ChangeDutyCycle(2.5)
        time.sleep(0.5)
        servo.stop()
        lockWrite(u'unlock')
        GPIO.cleanup()

def doCloseKeyOrder():
    servo = setservo()
    servo.start(0)
    servo.ChangeDutyCycle(7.25)
    time.sleep(0.5)
    servo.stop()
    lockWrite(u'lock')
    GPIO.cleanup()

# 「カギ開けて」「解錠して」等に反応する
@listen_to(u'(鍵|カギ)+.*(開|あけ|空け)+')
@listen_to(u'(解錠)+')
@listen_to(u'(open)+.*(door)+', re.IGNORECASE)
@respond_to(u'(鍵|カギ)+.*(開|あけ|空け)+')
@respond_to(u'(解錠)+')
@respond_to(u'(open)+.*(door)+', re.IGNORECASE)
def openKeyOrder(message, *something):
    # if カギが閉まっていたら :
    lock = lockRead()
    if lock == u'lock':

        doOpenKeyOrder()
        message.reply(u'わかりました。解錠します。')
    else:
        message.reply(u'鍵はすでに開いています。')

# 「鍵閉めて」「施錠」等の場合
@listen_to(u'(鍵|カギ)+.*(閉|しめ|締め)+')
@listen_to(u'(施錠)+')
@listen_to(u'(lock)+.*(door)+', re.IGNORECASE)
@respond_to(u'(鍵|カギ)+.*(閉|しめ|締め)+')
@respond_to(u'(施錠)+')
@respond_to(u'(lock)+.*(door)+', re.IGNORECASE)
def closeKeyOrder(message, *something):
    lock = lockRead()
    if lock == u'unlock':
        doCloseKeyOrder()
        message.reply(u'わかりました。施錠します。')

    else:
        message.reply(u'鍵はすでに閉まっています。')
