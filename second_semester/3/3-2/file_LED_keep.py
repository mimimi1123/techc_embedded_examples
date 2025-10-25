# -*- coding: utf-8 -*-
# ファイルを読み込みLEDを点灯させるプログラム
# 課題：このプログラムを使って，LEDを光らせる

from file_sample import file_read  # 関数を呼び出し
import RPi.GPIO as GPIO
import time

# ボタンとスイッチの設定（配線に合わせて変更）
SWITCH = 18   # 例: GPIO18 にスイッチ
LED    = 21   # 例: GPIO21 にLED

file_path = "led_state.txt"
data_read = ""

# GPIOセットアップ
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)

def parse_duration(s: str) -> float:
    """
    ファイル内容から点灯秒数を解釈する。
    - 数値: その秒数
    - "ON": 1秒
    - "OFF": 0秒（点灯しない）
    それ以外は0秒
    """
    if s is None:
        return 0.0
    t = s.strip().upper()
    if t == "ON":
        return 1.0
    if t == "OFF":
        return 0.0
    try:
        return float(t)
    except ValueError:
        return 0.0

# 以下のプログラムは変更せずにLEDを光らせる
try:
    while True:
        GPIO.output(LED, GPIO.LOW)  # いったん消灯

        if GPIO.input(SWITCH) == GPIO.HIGH:
            data_read = file_read(file_path)   # ファイルを読む:contentReference[oaicite:1]{index=1}
            duration  = parse_duration(data_read)

            # 点灯して指定秒数待つ（0なら実質スキップ）
            if duration > 0:
                GPIO.output(LED, GPIO.HIGH)
                time.sleep(duration)

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
