import RPi.GPIO as GPIO
import time

class MotorDriver:
    def __init__(self, pwm_pin, dir_pin1, dir_pin2, frequency=1000):
        self.pwm_pin = pwm_pin
        self.dir_pin1 = dir_pin1
        self.dir_pin2 = dir_pin2
        
        GPIO.setup(self.pwm_pin, GPIO.OUT)
        GPIO.setup(self.dir_pin1, GPIO.OUT)
        GPIO.setup(self.dir_pin2, GPIO.OUT)
        
        self.pwm = GPIO.PWM(self.pwm_pin, frequency)
        self.pwm.start(0)

    def set_speed(self, speed_pwm):
        duty = min(max(abs(speed_pwm), 0), 100)
        
        if speed_pwm > 0:
            GPIO.output(self.dir_pin1, GPIO.HIGH)
            GPIO.output(self.dir_pin2, GPIO.LOW)
        elif speed_pwm < 0:
            GPIO.output(self.dir_pin1, GPIO.LOW)
            GPIO.output(self.dir_pin2, GPIO.HIGH)
        else:
            GPIO.output(self.dir_pin1, GPIO.LOW)
            GPIO.output(self.dir_pin2, GPIO.LOW)
            
        self.pwm.ChangeDutyCycle(duty)

    def stop(self):
        self.pwm.stop()
        GPIO.output(self.dir_pin1, GPIO.LOW)
        GPIO.output(self.dir_pin2, GPIO.LOW)

# --- 以下テストコード ---
if __name__ == "__main__":
    # ピン設定
    PIN_PWM = 18
    PIN_IN1 = 22
    PIN_IN2 = 23

    GPIO.setmode(GPIO.BCM)
    
    try:
        motor = MotorDriver(PIN_PWM, PIN_IN1, PIN_IN2)
        print("モータ動作テスト開始")
        
        print("正転 (50%)")
        motor.set_speed(50)
        time.sleep(2)
        
        print("停止")
        motor.set_speed(0)
        time.sleep(1)
        
        print("逆転 (-50%)")
        motor.set_speed(-50)
        time.sleep(2)
        
        print("停止")
        motor.set_speed(0)
        
    except KeyboardInterrupt:
        print("\n強制終了")
    finally:
        motor.stop()
        GPIO.cleanup()
        print("GPIO cleanup 完了")