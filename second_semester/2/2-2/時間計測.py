import time
import RPi.GPIO as GPIO

time_start = time.time()#時間の計測開始

try:
	"""
	間に時間を計測したい処理を入れる
	例：
	time.sleep(2)
	"""
	
except KeyboardInterrupt:
	pass
	
finally:
	time_end = time.time()#時間の計測終了
	time_execution = time_end - time_start#かかった時間の計算
	print(time_execution)#結果の表示
	input():
	GPIO.cleanup()
