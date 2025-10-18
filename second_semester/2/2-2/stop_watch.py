import RPi.GPIO as GPIO
import time

# GPIOピンの番号（例）
BUTTON1_PIN = 18  # 開始・停止用ボタン
BUTTON2_PIN = 23  # リセット・ラップ用ボタン

# 初期設定
GPIO.setmode(GPIO.BCM)
GPIO.setup(BUTTON1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(BUTTON2_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)


# ストップウォッチの状態管理をする変数の定義
running = False
start_time = 0#開始時間
elapsed_time = 0#経過時間
lap_times = []#ラップ時間


#コールバック関数の定義
# 開始・停止ボタンのコールバック関数を定義
def start_stop_callback(channel):
    global is_running, start_time, elapsed_time
  　#global：関数の中でグローバル変数を呼び出せるようにする

    if is_running:
        # 停止
        elapsed_time += time.time() - start_time#停止時の経過時間を保存
        is_running = False
    else:
        # 開始
        
        
        start_time = time.time()#開始時の時間を保存
        is_running = True


# リセット・ラップボタンのコールバック関数を定義
def reset_lap_callback(channel):
    global is_running, elapsed_time, lap_times, start_time
  　#global：関数の中でグローバル変数を呼び出せるようにする

    if is_running:
        # ラップタイムを記録
        current_time = time.time() - start_time + elapsed_time
        lap_times.append(current_time)
    else:
        # リセット
        elapsed_time = 0
        lap_times = []


# 割り込み処理をを開始
GPIO.add_event_detect(BUTTON1_PIN, GPIO.FALLING, callback=button1_callback, bouncetime=300)
GPIO.add_event_detect(BUTTON2_PIN, GPIO.FALLING, callback=button2_callback, bouncetime=300)


try:
    # メインループ
    while True:
        # ターミナルの画面をクリアする関数
        os.system('clear')
        
        # 経過時間の表示
        if is_running:
            current_time = time.time() - start_time + elapsed_time#停止時間
        else:
            current_time = elapsed_time
        print(f"経過時間: {current_time:.2f} 秒")
        
        # ラップタイムの表示
        for i, lap in enumerate(lap_times, start=1):
            print(f"ラップ {i}: {lap:.2f} 秒")

        time.sleep(0.1)  # 表示更新の間隔
        
except KeyboardInterrupt:
    # プログラム終了時にGPIOをクリーンアップ
    GPIO.cleanup()
    print("\nプログラム終了")
