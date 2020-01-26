# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re
# import RPi.GPIO as GPIO
import time
import pigpio
lock = True
# GPIO.setmode(GPIO.BCM)

#GPIO4を制御パルスの出力に設定
# gp_out=4
servo = 18
# GPIO.setup(gp_out, GPIO.OUT)

#「GPIO4出力」でPWMインスタンスを作成する。
#GPIO.PWM( [ピン番号] , [周波数Hz] )
#SG92RはPWMサイクル:20ms(=50Hz), 制御パルス:0.5ms〜2.4ms, (=2.5%〜12%)。
# servo = GPIO.PWM(gp_out, 50)
pi = pigpio.pi()

# ピンを出力に設定
pi.set_mode(servo, pigpio.OUTPUT)
#パルス出力開始。　servo.start( [デューティサイクル 0~100%] )
#とりあえずゼロ指定だとサイクルが生まれないので特に動かないっぽい？
# servo.start(0)

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
    #   servo.start(0)
      message.reply(u'わかりました。解錠します。')
    #  servo.ChangeDutyCycle(5)
    #   time.sleep(0.2)
    #   servo.ChangeDutyCycle(0)
    #   servo.stop()
      pi.set_servo_pulsewidth(servo, 1000)

      time.sleep(2)
      # pi.set_servo_pulsewidth(servo, 1500)
      # time.sleep(2)
      pi.stop()

    else:
      message.reply(u'鍵はすでに開いています。')
    # # 命令を出したユーザ名を取得することもできます。
    # userID = message.channel._client.users[message.body['user']][u'name']
    # print userID + 'さんの命令でカギを開けます'

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
      # servo.start(0)
      message.reply(u'わかりました。施錠します。')
      # servo.ChangeDutyCycle(10)
      # time.sleep(0.2)
      # servo.ChangeDutyCycle(0)
      # servo.stop()
      pi.set_servo_pulsewidth(servo, 2000)

      time.sleep(2)
      # pi.set_servo_pulsewidth(servo, 1500)
      # time.sleep(2)
      pi.stop()
      # 停止 (FS90Rは1.5msのパルスで停止)
    else:
      message.reply(u'鍵はすでに閉まっています。')