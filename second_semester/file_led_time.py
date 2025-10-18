# ボタンを押すとLEDが５秒間点灯するプログラム
# 課題：このプログラムに変更を加えてファイル内の秒数だけ点灯するようにせよ
from file_sample import file_read  # 関数を呼び出し
import RPi.GPIO as GPIO
import time

# ボタンとLEDのピン番号設定
SWITCH = 17  # スイッチのGPIOピン番号 (例)
LED = 27     # LEDのGPIOピン番号 (例)

file_path = "led_time.txt"  # ファイルパス（例）
data_read = ""

# GPIOセットアップ
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)

try:
    while True:
        if GPIO.input(SWITCH) == GPIO.HIGH:  # スイッチが押されたとき
			GPIO.output(LED, GPIO.HIGH)   # LEDを点灯
			time.sleep(5)        #5秒間の点灯
			GPIO.output(LED, GPIO.LOW)    # LEDを消灯

        time.sleep(0.05)

except KeyboardInterrupt:
    pass

finally:
    GPIO.cleanup()
