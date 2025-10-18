#ファイルを読み込みLEDを点灯させるプログラム
#課題：このプログラムを使って，LEDを光らせる
from file_sample import file_read #関数を呼び出し
import RPi.GPIO as GPIO
import time

#ボタンとスイッチの設定
SWITCH = 
LED = 

file_path = "led_state.txt"
data_read = ""

#GPIOセットアップ（省略）

#以下のプログラムは変更せずにLEDを光らせる
try:
	while True:
		GPIO.output(LED,GPIO.LOW)
		
		if GPIO.input(SWITCH) == GPIO.HIGH:
			data_read = file_read(file_path)
			int_data_read = int(data_read)#追加①
			
			GPIO.output(LED1,GPIO.HIGH)
			time.sleep(int_data_read) 
		
		time.sleep(0.05)

except KeyboardInterrupt:
	pass

finally:
	GPIO.cleanup()
