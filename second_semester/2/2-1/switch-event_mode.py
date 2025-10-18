import RPi.GPIO as GPIO # GPIOを利用する
import time             # sleepを利用する

# ポート番号の定義
SWITCH = 19
LED = 26
LED_BLINKING = 1
LED_LIGHTING = 2#モードの定義
led_mode = LED_BLINKING#モードを始めは点滅にしておく

# GPIOの初期化 --- (*1)
GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(LED, GPIO.OUT)


#コールバック関数の定義
def callback_change_switch(ch):
    global led_value
    print("callback", ch)
    if ch != SWITCH: return
    if led_mode == LED_BLINKING:
        led_mode = LED_LIGHTING
    else:
        led_mode = LED_BLINKING


# イベントを設定 --- (*3)
GPIO.add_event_detect(
    SWITCH, # ポート番号 
    GPIO.RISING, # イベントの種類
    callback=callback_change_switch, # 関数の指定
    bouncetime=200) # 連続イベントを制限

# LEDを消灯しておく
GPIO.output(LED, GPIO.LOW)


try:
    while True:
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
