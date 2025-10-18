# -*- coding: utf-8 -*-
# ファイルを読み込みLEDを点灯させるプログラム
# 課題：このプログラムを使って，LEDを光らせる

from file_sample import file_read  # 関数を呼び出し
import RPi.GPIO as GPIO
import time

# ボタンとLEDピンの設定（自分の回路に合わせて変更）
SWITCH = 18  # 例: GPIO18 にスイッチを接続
LED = 21     # 例: GPIO21 にLEDを接続

file_path = "led_state.txt"
data_read = ""

# GPIOセットアップ
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)

# 以下のプログラムは変更せずにLEDを光らせる
try:
    while True:
        if GPIO.input(SWITCH) == GPIO.HIGH:
            data_read = file_read(file_path)

        if data_read == "ON":
            GPIO.output(LED, GPIO.HIGH)
        else:
            GPIO.output(LED, GPIO.LOW)

        time.sleep(0.5)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
