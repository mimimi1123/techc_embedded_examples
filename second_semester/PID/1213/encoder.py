import RPi.GPIO as GPIO
import time

class Encoder:
    def __init__(self, pin_a, pin_b):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.count = 0
        self.last_a = 0
        self.last_b = 0
        
        # GPIO.setmodeは呼び出し元で行う前提だが、
        # クラス内で安全のためsetup前に現在のモードを確認することも可能。
        # ここではシンプルにsetupのみ行う。
        GPIO.setup(self.pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # 初期状態を読み取る
        self.last_a = GPIO.input(self.pin_a)
        self.last_b = GPIO.input(self.pin_b)
        
        GPIO.add_event_detect(self.pin_a, GPIO.BOTH, callback=self.update_count)
        GPIO.add_event_detect(self.pin_b, GPIO.BOTH, callback=self.update_count)

    def update_count(self, channel):
        state_a = GPIO.input(self.pin_a)
        state_b = GPIO.input(self.pin_b)
        
        # グレイコード方式でエンコーダの回転方向を判定
        if self.last_a == 0 and self.last_b == 0:
            if state_a == 1:
                self.count += 1
            elif state_b == 1:
                self.count -= 1
        elif self.last_a == 1 and self.last_b == 0:
            if state_b == 1:
                self.count += 1
            elif state_a == 0:
                self.count -= 1
        elif self.last_a == 1 and self.last_b == 1:
            if state_a == 0:
                self.count += 1
            elif state_b == 0:
                self.count -= 1
        elif self.last_a == 0 and self.last_b == 1:
            if state_b == 0:
                self.count += 1
            elif state_a == 1:
                self.count -= 1
        
        self.last_a = state_a
        self.last_b = state_b

    def get_count(self):
        return self.count
    
    def reset_count(self):
        self.count = 0

# --- 以下テストコード ---
if __name__ == "__main__":
    # ピン設定 (環境に合わせて変更してください)
    PIN_A = 17
    PIN_B = 27

    GPIO.setmode(GPIO.BCM)
    
    try:
        enc = Encoder(PIN_A, PIN_B)
        print("エンコーダテスト開始。軸を手で回してください。")
        print("停止するには Ctrl+C を押してください。")
        
        last_count = 0
        while True:
            current_count = enc.get_count()
            if current_count != last_count:
                print(f"Count: {current_count}")
                last_count = current_count
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\nテスト終了")
    finally:
        GPIO.cleanup()