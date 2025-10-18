import RPi.GPIO as GPIO # GPIOを利用する
import time             # sleepを利用する

# ポート番号の定義
SWITCH = 18
LED = 21
LED_BLINKING = 1#モードの定義
LED_LIGHTING = 2#モードの定義
led_mode = LED_BLINKING

# GPIOの初期化 --- (*1)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)

# LEDを消灯する
GPIO.output(LED, GPIO.LOW)

try:
    while True:
		if GPIO.input(SWITCH):#ポーリング
			if led_mode == LED_BLINKING:
				led_mode = LED_LIGHTING#点灯
			else:
				led_mode = LED_BLINKING#点滅
			
		if led_mode == LED_BLINKING:
			GPIO.output(LED, GPIO.HIGH)
			time.sleep(0.5)
			GPIO.output(LED, GPIO.LOW)
			time.sleep(0.5)
		else:
			GPIO.output(LED, GPIO.HIGH)
			time.sleep(0.5)

except KeyboardInterrupt:
    GPIO.cleanup()

