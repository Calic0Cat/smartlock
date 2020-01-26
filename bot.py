# -*- coding: utf-8 -*-
from slackbot.bot import Bot
from threading import Thread
import binascii
import nfc
import time
import TestSlackBotPlugin as SBP

def IDReader(parameter_list):
    # -*- coding: utf-8 -*-
    
    # Suica待ち受けの1サイクル秒
    TIME_cycle = 1.0
    # Suica待ち受けの反応インターバル秒
    TIME_interval = 0.2
    # タッチされてから次の待ち受けを開始するまで無効化する秒
    TIME_wait = 3

    # NFC接続リクエストのための準備
    # 212F(FeliCa)で設定
    target_req_suica = nfc.clf.RemoteTarget("212F")
    # 0003(Suica)
    target_req_suica.sensf_req = bytearray.fromhex("0000030000")
    try:
        while True:
        # USBに接続されたNFCリーダに接続してインスタンス化
        clf = nfc.ContactlessFrontend('usb')
        # Suica待ち受け開始
        # clf.sense( [リモートターゲット], [検索回数], [検索の間隔] )
        target_res = clf.sense(target_req_suica, iterations=int(TIME_cycle//TIME_interval)+1 , interval=TIME_interval)

            if target_res != None:

                tag = nfc.tag.activate_tt3(clf, target_res)
                tag.sys = 3

                #IDmを取り出す
                idm = binascii.hexlify(tag.idm)

                time.sleep(TIME_wait)
            if SBP.lockRead() == "lock":
                SBP.doOpenKeyOrder()
            else :
                SBP.doCloseKeyOrder()
    except KeyboardInterrupt:
      
        

    clf.close()

# SlackBot起動
if __name__ == "__main__":
    paspi_doorlock_bot = Bot()

    paspi_doorlock_bot.run()

