import RPi.GPIO as GPIO # GPIOを利用する
import time             # sleepを利用する

# ポート番号の定義
SWITCH = 18
LED = 21
LED_BLINKING = 1#モードの定義
LED_LIGHTING = 2#モードの定義
led_mode = LED_BLINKING
bouncetime = 0.2#連続のボタンの受付時間[sec]
time_switch_previous = 0#前回ボタンをおしてからの経過時間

# GPIOの初期化 
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)

# LEDを消灯する
GPIO.output(LED, GPIO.LOW)

time_mode_started = time.perf_counter()#最初のモードの開始時間

try:
    while True:
		time_now = time.perf_counter()						#今の時間の取得
		if GPIO.input(SWITCH):								#ボタンが押されているとき，
			if time_now - time_switch_previous > bouncetime:#前にボタンを押してから十分な時間が経っていたら，
				#モードの切り替え
				if led_mode == LED_BLINKING:				
					led_mode = LED_LIGHTING	#点灯へ
				else:
					led_mode = LED_BLINKING	#点滅へ
				time_switch_previous = time_now				#スイッチの状態を変更
				time_mode_started = time_now #モードの切り替わり時の更新

		time_mode_spent = time_now-time_mode_started#今のモードでの経過時間
		
		if led_mode == LED_BLINKING:	#点滅モードでの処理
			
			if  time_mode_spent < 0.5:		#今のモードで0.5秒が経っていないうちは，
				GPIO.output(LED, GPIO.HIGH)	#光る
			elif time_mode_spent < 1.0:		#今のモードで1.0秒が経っていないうちは，
				GPIO.output(LED, GPIO.LOW)	#消える
			else:							#今のモードで1.0秒経ったら時間をリセット
				time_mode_started = time_now
								
		elif led_mode == LED_LIGHTING:	#点灯モードでの処理
			GPIO.output(LED, GPIO.HIGH)#点灯し続ける
			"""
			この部分は点滅モード同様に以下のように実装しても良い
			if time_mode_spend < 0.5:
				GPIO.output(LED, GPIO.HIGH) #光る	
			else:							#今のモードで0.5秒経ったら時間をリセット
				time_mode_started = time_now
			
			"""
		
		time.sleep(0.005)#周期
			

except KeyboardInterrupt:
    GPIO.cleanup()

