import RPi.GPIO as GPIO # GPIOを利用する
import time             # sleepを利用する

# ポート番号の定義
SWITCH = 18
LED = 21
led_value = GPIO.LOW

# GPIOの初期化 --- (*1)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)

# スイッチの切り替えイベントの定義 --- (*2)
def callback_change_switch(ch):
    global led_value
    print("callback", ch)
    if ch != SWITCH: return#違うボタンが押されたときに何もしないためのif文
    if led_value == GPIO.LOW:
        GPIO.output(LED, )#①この行のプログラムを完成させる
        led_value = GPIO.HIGH
    else:
        GPIO.output(LED, )#②この行のプログラムを完成させる
        led_value = GPIO.LOW
        
# イベントの設定 --- (*3)
GPIO.add_event_detect(
    SWITCH, # ポート番号 
    GPIO.RISING, # イベントの種類
    callback=callback_change_switch, # 関数の指定
    bouncetime=200) # 連続イベントを制限

# LEDを消灯する
GPIO.output(LED, GPIO.LOW)

# プログラムが終わらないように待機 --- (*4)
try:
    while True:
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()

