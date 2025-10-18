import RPi.GPIO as GPIO # GPIOを利用する
import time             # sleepを利用する

# ポート番号の定義
SWITCH = 18
LED = 21
led_value = GPIO.LOW
time_now = 0
time_start = 0

# GPIOの初期化 --- (*1)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)

# スイッチの切り替えイベントの定義 --- (*2)
def callback_change_switch(ch):
    global led_value
    global time_now = time.time()#ボタンを押した時間を記録
    print("callback", ch)
    print("time", time_start-time_now)#呼び出しの時間（秒）を表示
    if ch != SWITCH: return
    if led_value == GPIO.LOW:
        led_value = GPIO.HIGH
    else:
        led_value = GPIO.LOW

# LEDを消灯する
GPIO.output(LED, GPIO.LOW)

time_start = time.time()#処理の開始時間を取得
        
# イベントの設定 --- (*3)
GPIO.add_event_detect(
    SWITCH, # ポート番号 
    GPIO.RISING, # イベントの種類
    callback=callback_change_switch, # 関数の指定
    bouncetime=200) # 連続イベントを制限

# プログラムが終わらないように待機 --- (*4)
try:
    while True:
		if led_value == GPIO.HIGH:
			
		else:
			
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()

