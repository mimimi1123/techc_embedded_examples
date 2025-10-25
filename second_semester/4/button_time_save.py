# -*- coding: utf-8 -*-
import time
import numpy as np
import RPi.GPIO as GPIO

# ===== 設定 =====
SWITCH = 18
CSV_FILE = "button_durations.csv"
DEBOUNCE_MS = 50  # チャタリング防止
# ===============

GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

last_state = GPIO.input(SWITCH)
last_change = time.time()
pressed_at = None

# NumPy配列（空の2D配列: 列は [start, end, duration]）
data = np.empty((0, 3), dtype=np.float64)

print("計測を開始します。Ctrl+C で終了します。")

try:
    while True:
        now = time.time()
        state = GPIO.input(SWITCH)

        # チャタリング防止
        if state != last_state and (now - last_change) * 1000.0 >= DEBOUNCE_MS:
            last_change = now
            last_state = state

            if state == GPIO.HIGH:
                pressed_at = now
            else:
                if pressed_at is not None:
                    duration = now - pressed_at
                    # 新しい行を NumPy 配列に追加
                    new_row = np.array([[pressed_at, now, duration]])
                    data = np.vstack((data, new_row))

                    print(f"start={pressed_at:.3f}, end={now:.3f}, duration={duration:.3f}s")
                    pressed_at = None
        time.sleep(0.005)

except KeyboardInterrupt:
    print("\n計測を終了します。")

    # 計測結果の表示
    if data.size > 0:
        print(f"記録件数: {len(data)}")
        print("最後のデータ:", data[-1])

        # NumPyでCSV保存
        header = "start_time,end_time,duration"
        np.savetxt(CSV_FILE, data, delimiter=",", header=header, comments="", fmt="%.6f")
        print(f"データを {CSV_FILE} に保存しました。")
    else:
        print("保存するデータがありません。")

finally:
    GPIO.cleanup()
