import RPi.GPIO as GPIO # GPIOを利用する
import time             # sleepを利用する

# ポート番号の定義
SWITCH = 18
LED = 21
led_value = GPIO.LOW
time_now = 0
time_start = 0

# GPIOの初期化 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)


# スイッチの切り替えイベント関数の定義
def callback_change_switch(ch):
    global led_value #globalは関数内でグローバル変数を操作可能にする
    global time_now = time.time()#ボタンを押した時間を記録
    print("callback", ch)
    if ch != SWITCH: 
		print("incorrect switch is pushed!")
		return#呼び出したボタンが違うときに処理をしないためのプログラム
    time_spent = #穴埋め①：かかった時間を計算
    print("time", time_spent)#呼び出しの時間（秒）を表示
    #LEDの状態の切り替え
    if led_value == GPIO.LOW:
        led_value = GPIO.HIGH
    else:
        led_value = GPIO.LOW



GPIO.output(LED, GPIO.LOW)# LEDを消灯しておく
time_start = time.time()#処理の開始時間を取得
        
# イベント（割り込み）の開始
GPIO.add_event_detect(
    SWITCH, # ポート番号 
    GPIO.RISING, # イベントの種類
    callback=callback_change_switch, # 関数の指定
    bouncetime=200) # 連続イベントを制限


try:
	#メインループ
    while True:
		if led_value == GPIO.HIGH:
			#穴埋め②led_valueがHIGHの状態のとき
		else:
			#穴埋め③led_valueがLOWの状態のとき
        time.sleep(0.1)

except KeyboardInterrupt:
    GPIO.cleanup()

