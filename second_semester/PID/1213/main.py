import RPi.GPIO as GPIO
import time
from encoder import Encoder
from motor_driver import MotorDriver
from pid_controller import PIDController

# ピン設定
PIN_ENC_A = 17
PIN_ENC_B = 27
PIN_PWM = 18
PIN_IN1 = 22
PIN_IN2 = 23

# 定数設定
PPR = 11 * 90  # パルス数(11) × ギア比(90: JGB37-520の例) ※データシート要確認
TARGET_RPM = 60  # 目標回転数

def main():
    GPIO.setmode(GPIO.BCM)
    
    try:
        # インスタンス化
        encoder = Encoder(PIN_ENC_A, PIN_ENC_B)
        motor = MotorDriver(PIN_PWM, PIN_IN1, PIN_IN2)
        # PIDゲイン調整 (Kp, Ki, Kd) - 実際の挙動を見て調整が必要です
        pid = PIDController(kp=1.0, ki=0.5, kd=0.01)

        prev_time = time.time()
        prev_count = 0

        print(f"Start PID Control. Target: {TARGET_RPM} RPM")

        while True:
            current_time = time.time()
            dt = current_time - prev_time
            
            # 制御周期（例: 0.1秒ごと）
            if dt >= 0.1:
                # 1. 現在の速度(RPM)を計算
                current_count = encoder.get_count()
                delta_count = current_count - prev_count
                
                # (パルス変化量 / 1回転あたりのパルス数) / 時間(分)
                current_rpm = (delta_count / PPR) / (dt / 60)
                
                # 2. PID計算 (目標RPM - 現在RPM) -> 操作量PWM(-100~100)
                control_output = pid.compute(TARGET_RPM, current_rpm, dt)

                # rpm to PWM
                #6v 100rpm
                duty = control_output / 100 

                # 3. モータ駆動
                motor.set_speed(control_output)
                
                # デバッグ表示
                print(f"Target: {TARGET_RPM}, RPM: {current_rpm:.2f}, PWM: {control_output:.2f}")
                
                # 次のループのために値を更新
                prev_time = current_time
                prev_count = current_count

            time.sleep(0.01) # CPU負荷を下げるための短いスリープ

    except KeyboardInterrupt:
        print("Stopping...")
    finally:
        motor.stop()
        GPIO.cleanup()

if __name__ == "__main__":
    main()