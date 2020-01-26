# -*- coding: utf-8 -*-
import binascii
import nfc
import time
from threading import Thread, Timer

# -*- coding: utf-8 -*-
from slackbot.bot import respond_to, listen_to
import re
import RPi.GPIO as GPIO
import time
lock = True
# GPIO.setmode(GPIO.BCM)

# #GPIO4を制御パルスの出力に設定
# gp_out=4
# GPIO.setup(gp_out, GPIO.OUT)
# servo = GPIO.PWM(gp_out, 50)
#「GPIO4出力」でPWMインスタンスを作成する。
#GPIO.PWM( [ピン番号] , [周波数Hz] )
#SG92RはPWMサイクル:20ms(=50Hz), 制御パルス:0.5ms〜2.4ms, (=2.5%〜12%)。


# ピンを出力に設定
# pi.set_mode(servo, pigpio.OUTPUT)
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

# Suica待ち受けの1サイクル秒
TIMECYCLE = 1.0
# Suica待ち受けの反応インターバル秒
TIMEINTERVAL = 0.2
# タッチされてから次の待ち受けを開始するまで無効化する秒
TIMEWAIT = 3

# NFC接続リクエストのための準備
# 212F(FeliCa)で設定
suica = nfc.clf.RemoteTarget("212F")
# 0003(Suica)
suica.sensf_req = bytearray.fromhex("0000030000")

print 'Suica waiting...'
while True:
    # USBに接続されたNFCリーダに接続してインスタンス化
    clf = nfc.ContactlessFrontend('usb')
    # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
    target_res = clf.sense(suica, iterations=int(TIMECYCLE//TIMEINTERVAL)+1 , interval=TIMEINTERVAL)

    if target_res != None:

        tag = nfc.tag.activate_tt3(clf, target_res)
        tag.sys = 3

        #IDmを取り出す
        idm = binascii.hexlify(tag.idm)

        time.sleep(TIMEWAIT)

    clf.close()

