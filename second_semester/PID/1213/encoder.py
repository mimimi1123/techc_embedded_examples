import RPi.GPIO as GPIO
import time

class Encoder:
    def __init__(self, pin_a, pin_b):
        self.pin_a = pin_a
        self.pin_b = pin_b
        self.count = 0
        self.last_state = 0
        
        # GPIO.setmodeは呼び出し元で行う前提だが、
        # クラス内で安全のためsetup前に現在のモードを確認することも可能。
        # ここではシンプルにsetupのみ行う。
        GPIO.setup(self.pin_a, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        GPIO.setup(self.pin_b, GPIO.IN, pull_up_down=GPIO.PUD_UP)
        
        # 初期状態を2bitで保持 (A:bit1, B:bit0)
        self.last_state = (GPIO.input(self.pin_a) << 1) | GPIO.input(self.pin_b)
        
        # 双方の立ち上がり/立ち下がりを割り込みで監視
        GPIO.add_event_detect(self.pin_a, GPIO.BOTH, callback=self.update_count, bouncetime=1)
        GPIO.add_event_detect(self.pin_b, GPIO.BOTH, callback=self.update_count, bouncetime=1)

    def update_count(self, channel):
        state_a = GPIO.input(self.pin_a)
        state_b = GPIO.input(self.pin_b)
        state = (state_a << 1) | state_b

        # グレイコードの遷移表 (前状態->現状態で+1/-1/0を与える)
        transition = {
            0b00: {0b01: 1, 0b10: -1},
            0b01: {0b11: 1, 0b00: -1},
            0b11: {0b10: 1, 0b01: -1},
            0b10: {0b00: 1, 0b11: -1},
        }

        delta = transition.get(self.last_state, {}).get(state, 0)
        self.count += delta
        self.last_state = state

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