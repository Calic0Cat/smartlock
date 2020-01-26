# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re
import RPi.GPIO as GPIO
import time
lock = True

# 「カギ開けて」「解錠して」等に反応するようにします
@listen_to(u'(鍵|カギ)+.*(開|あけ|空け)+')
@listen_to(u'(解錠)+')
@listen_to('(open)+.*(door)+', re.IGNORECASE)
@respond_to(u'(鍵|カギ)+.*(開|あけ|空け)+')
@respond_to(u'(解錠)+')
@respond_to('(open)+.*(door)+', re.IGNORECASE)
def openKeyOrder(message, *something):
    # if カギが閉まっていたら :
    if lock:
      GPIO.setmode(GPIO.BCM)

      #GPIO4を制御パルスの出力に設定
      gp_out=4
      GPIO.setup(gp_out, GPIO.OUT)
      servo = GPIO.PWM(gp_out, 50)

      servo.start(0)
      message.reply(u'わかりました。解錠します。')
      servo.ChangeDutyCycle(2.5)
      time.sleep(0.5)
      # servo.ChangeDutyCycle(0)
      servo.stop()
      GPIO.cleanup()
    else:
      message.reply(u'鍵はすでに開いています。')

# 「鍵閉めて」「施錠」等の場合はこちら
@listen_to(u'(鍵|カギ)+.*(閉|しめ|締め)+')
@listen_to(u'(施錠)+')
@listen_to('(lock)+.*(door)+', re.IGNORECASE)
@respond_to(u'(鍵|カギ)+.*(閉|しめ|締め)+')
@respond_to(u'(施錠)+')
@respond_to('(lock)+.*(door)+', re.IGNORECASE)
def closeKeyOrder(message, *something):
    # 以下openと同じなので省略
    if lock:
      GPIO.setmode(GPIO.BCM)

      #GPIO4を制御パルスの出力に設定
      gp_out=4
      GPIO.setup(gp_out, GPIO.OUT)
      servo = GPIO.PWM(gp_out, 50)
      servo.start(0)
      message.reply(u'わかりました。施錠します。')
      servo.ChangeDutyCycle(7.25)
      time.sleep(0.5)
      # servo.ChangeDutyCycle(0)
      servo.stop()
      GPIO.cleanup()

    else:
      message.reply(u'鍵はすでに閉まっています。')