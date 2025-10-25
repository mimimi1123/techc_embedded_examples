import time
import csv
import RPi.GPIO as GPIO

SWITCH = 18
CSV_FILE = "button_durations.csv"
DEBOUNCE_MS = 50

GPIO.setmode(GPIO.BCM)
GPIO.setup(SWITCH, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

last_state = GPIO.input(SWITCH)
last_change = time.time()
pressed_at = None

print("計測を開始します。Ctrl+C で終了します。")

try:
    while True:
        now = time.time()
        state = GPIO.input(SWITCH)
        if state != last_state and (now - last_change) * 1000.0 >= DEBOUNCE_MS:
            last_change = now
            last_state = state
            if state == GPIO.HIGH:
                pressed_at = now
            else:
                if pressed_at is not None:
                    duration = now - pressed_at
                    with open(CSV_FILE, "a", newline="", encoding="utf-8") as f:
                        writer = csv.writer(f)
                        writer.writerow([f"{pressed_at:.6f}", f"{now:.6f}", f"{duration:.6f}"])
                    print(f"saved: start={pressed_at:.3f}, end={now:.3f}, duration={duration:.3f}s -> {CSV_FILE}")
                    pressed_at = None
        time.sleep(0.005)
except KeyboardInterrupt:
    print("\n終了します。")
finally:
    GPIO.cleanup()
