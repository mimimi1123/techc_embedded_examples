#!/usr/bin/env python3
import RPi.GPIO as GPIO
import time
import math

# ==== ユーザ設定ここから ====
PIN_ENC_A = 17   # A相 BCM
PIN_ENC_B = 27   # B相 BCM

PULSES_PER_REV_MOTOR = 11   # モータ側PPR（A/Bの1相1エッジ基準）
GEAR_RATIO = 50             # モータ : 出力軸 = 1 : 50

# ここでは「4連番」でカウントする（A/B両相の立ち上がり/立ち下がり）
COUNTS_PER_REV_OUTPUT = PULSES_PER_REV_MOTOR * 4 * GEAR_RATIO
# ==== ユーザ設定ここまで ====


encoder_count = 0       # 出力軸カウント
prev_state = 0          # 前回のAB状態 (0b00〜0b11)


# エンコーダのA/B相のエッジを検出するコールバック関数
# A相、B相のいずれかの立ち上がり/立ち下がりで呼ばれる
def encoder_callback(channel):
    global encoder_count, prev_state

    a = GPIO.input(PIN_ENC_A)
    b = GPIO.input(PIN_ENC_B)
    state = (a << 1) | b          # 0b00,0b01,0b10,0b11 のどれか

    # 前状態(2bit)と現状態(2bit)を4bitにまとめる
    transition = (prev_state << 2) | state

    # 正方向の遷移パターン
    if transition in (0b0001,  # 00 -> 01
                      0b0111,  # 01 -> 11
                      0b1110,  # 11 -> 10
                      0b1000): # 10 -> 00
        encoder_count += 1

    # 逆方向の遷移パターン
    elif transition in (0b0010,  # 00 -> 10
                        0b0100,  # 10 -> 11
                        0b1101,  # 11 -> 01
                        0b1011): # 01 -> 00
        encoder_count -= 1

    # それ以外の(飛び越えやチャタリング)は無視

    prev_state = state


def main():
    global prev_state, encoder_count

    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_ENC_A, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    GPIO.setup(PIN_ENC_B, GPIO.IN, pull_up_down=GPIO.PUD_UP)

    # 初期状態を読んでおく
    prev_state = (GPIO.input(PIN_ENC_A) << 1) | GPIO.input(PIN_ENC_B)

    # A/B両方、立ち上がり/立ち下がり両エッジを検出
    GPIO.add_event_detect(PIN_ENC_A, GPIO.BOTH, callback=encoder_callback)
    GPIO.add_event_detect(PIN_ENC_B, GPIO.BOTH, callback=encoder_callback)

    print("Start")

    last_time = time.monotonic()
    last_count = encoder_count

    try:
        while True:
            time.sleep(0.1)  # 100msごとに表示

            now = time.monotonic()
            dt = now - last_time
            current_count = encoder_count

            delta_count = current_count - last_count
            revs = delta_count / COUNTS_PER_REV_OUTPUT      # [rev] / dt
            omega = revs * 2.0 * math.pi / dt               # [rad/s]

            angle = (current_count / COUNTS_PER_REV_OUTPUT) * 2.0 * math.pi

            print(f"ω = {omega:8.4f} rad/s, angle = {angle:8.4f} rad, count = {current_count}")

            last_time = now
            last_count = current_count

    except KeyboardInterrupt:
        print("\n終了します")

    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
