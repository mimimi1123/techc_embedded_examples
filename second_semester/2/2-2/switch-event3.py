import RPi.GPIO as GPIO # GPIOを利用する
import time             # sleepを利用する

# ピン番号の定義（BCM）
SWITCH = 18								
LED = 21								
led_state = GPIO.LOW					#LEDの初期状態を設定

# GPIOの初期化 --- (*1)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)


# スイッチが押されたときのコールバック関数を設定 --- (*2)
def callback_change_switch(ch):
    global led_state					
    print("callback", ch)			#押されたボタンをターミナルに表示
    #現在のled_stateに応じて条件分岐
    if led_state == GPIO.LOW:			
        led_state = GPIO.HIGH
    else:
        led_state = GPIO.LOW

        
# イベントの設定 --- (*3)
GPIO.add_event_detect(
    SWITCH, 							# ポート番号 
    GPIO.RISING, 						# イベントの種類（押したとき）
    callback=callback_change_switch, 	# コールバック関数の指定
    bouncetime=200) 					# 次に反応するまでの時間[ms]


try:
	# メインループ：cntr+Cが押されるまで実行を繰り返す --- (*4)
    while True:
		GPIO.output(LED,led_state)		#現在のled_stateに応じて出力
        time.sleep(0.1)

except KeyboardInterrupt:				#cntr+Cが押されたときの処理
    GPIO.cleanup()

