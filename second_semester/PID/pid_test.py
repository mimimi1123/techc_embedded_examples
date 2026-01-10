"""
簡単なモータモデルを用いた PID 速度制御 学習用プログラム

【できること】
・画面下部のスライダーから Kp, Ki, Kd をリアルタイムに変更
・Setpoint スライダーで目標速度をリアルタイムに変更
・目標値（破線）と実際のモータ速度（実線）をリアルタイムでプロット

【前提】
pip install matplotlib
で matplotlib を入れてから実行してください。

python pid_motor_sim.py
などで実行するとウィンドウが立ち上がります。
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# ==============================
# モータ＋PID 制御の簡単なモデル
# ==============================

class MotorPIDSim:
    """
    非常に簡略化した 1 次遅れモータモデル + PID 制御器

    モータモデル:
        τ * dv/dt + v = K * u
    という 1 次遅れ系をオイラー法で離散化して使います。

    v : モータの角速度 (ここでは無次元化して 0〜1 程度を想定)
    u : 制御入力（電圧のイメージ）
    τ : 時定数
    K : ゲイン
    """

    def __init__(self, dt=0.01, tau=0.2, K_motor=1.0):
        # シミュレーション刻み時間 [s]
        self.dt = dt

        # モータの物理パラメータ（ここでは適当な値）
        self.tau = tau
        self.K_motor = K_motor

        # 状態量
        self.v = 0.0           # モータ速度
        self.t = 0.0           # 時間

        # PID 内部状態
        self.integral = 0.0    # 積分成分
        self.prev_error = 0.0  # ひとつ前の偏差

        # プロット用履歴
        self.history_t = [0.0]
        self.history_v = [0.0]
        self.history_ref = [0.0]

    def step(self, setpoint, Kp, Ki, Kd):
        """
        1 ステップ分、PID 制御 + モータ応答を進める

        setpoint : 目標速度
        Kp, Ki, Kd : PID ゲイン
        """

        dt = self.dt

        # ---- PID 制御器 ----
        # 偏差 = 目標値 - 現在値
        error = setpoint - self.v

        # 積分（台形近似ではなく単純なオイラー積分）
        self.integral += error * dt

        # 微分（偏差の差分 / dt）
        derivative = (error - self.prev_error) / dt

        # PID 出力（制御入力 u）
        u = Kp * error + Ki * self.integral + Kd * derivative

        # ---- モータモデル ----
        # τ * dv/dt + v = K * u  → dv/dt = (-v + K*u) / τ
        dv = dt * ((-self.v + self.K_motor * u) / self.tau)
        self.v += dv

        # 状態更新
        self.prev_error = error
        self.t += dt

        # 履歴に追加（グラフ描画用）
        self.history_t.append(self.t)
        self.history_v.append(self.v)
        self.history_ref.append(setpoint)


# ==============================
# グラフと UI（スライダー）の準備
# ==============================

def main():
    # シミュレータ本体
    sim = MotorPIDSim(dt=0.005, tau=0.2, K_motor=1.0)

    # 初期値（PID ゲインと目標値）
    init_Kp = 2.0
    init_Ki = 0.5
    init_Kd = 0.01
    init_setpoint = 0.5

    # プロット用 Figure / Axes を作成
    fig, ax = plt.subplots()
    # 下側に UI (スライダー) を置くスペースを確保
    plt.subplots_adjust(left=0.1, bottom=0.35)

    # 最初に 1 点だけ描画（後でリアルタイムに更新）
    (line_v,) = ax.plot(sim.history_t, sim.history_v, label="Motor speed")
    (line_ref,) = ax.plot(sim.history_t, sim.history_ref, "--", label="Target speed")

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Speed")
    ax.legend(loc="upper right")

    # x 軸・y 軸の初期範囲
    ax.set_xlim(0, 5)
    ax.set_ylim(-1.0, 1.5)

    # -------------------------
    # スライダー UI の作成
    # -------------------------
    # スライダーを置く枠（Axes）を作る
    # [left, bottom, width, height] の順（0〜1 の相対座標）
    axcolor = "lightgoldenrodyellow"

    ax_Kp = plt.axes([0.1, 0.25, 0.8, 0.03], facecolor=axcolor)
    ax_Ki = plt.axes([0.1, 0.20, 0.8, 0.03], facecolor=axcolor)
    ax_Kd = plt.axes([0.1, 0.15, 0.8, 0.03], facecolor=axcolor)
    ax_sp = plt.axes([0.1, 0.08, 0.8, 0.03], facecolor=axcolor)

    # スライダー本体
    # valmin, valmax はとりあえずそれっぽい範囲にしてあるので、
    # 実際に試しながら調整して構いません。
    s_Kp = Slider(ax_Kp, "Kp", 0.0, 10.0, valinit=init_Kp)
    s_Ki = Slider(ax_Ki, "Ki", 0.0, 5.0, valinit=init_Ki)
    s_Kd = Slider(ax_Kd, "Kd", 0.0, 2.0, valinit=init_Kd)
    s_sp = Slider(ax_sp, "Setpoint", -1.0, 1.0, valinit=init_setpoint)

    # ==============================
    # タイマーで定期的にシミュレーション＋描画
    # ==============================

    # どのくらいの間隔で描画を更新するか [ms]
    # dt=0.005s で内部ステップを 10 回ずつ進めるので
    # 1 フレームあたり 0.05s 進むイメージ
    interval_ms = 50

    def update_sim(_):
        """
        タイマーコールバック：PID & モータを少し進めて、曲線を描き直す
        """

        # スライダーの値を読み取る（リアルタイムにゲイン・目標値変更）
        Kp = s_Kp.val
        Ki = s_Ki.val
        Kd = s_Kd.val
        setpoint = s_sp.val

        # シミュレーションを何ステップか進める
        # （1 回の描画更新あたりに少し時間を進める）
        for _ in range(10):
            sim.step(setpoint, Kp, Ki, Kd)

        # グラフのデータを更新
        line_v.set_data(sim.history_t, sim.history_v)
        line_ref.set_data(sim.history_t, sim.history_ref)

        # x 軸は「直近の 5 秒間」だけを見るようにスクロール
        t_now = sim.t
        ax.set_xlim(max(0, t_now - 5.0), t_now)

        # y 軸は速度に合わせて少し広くとる（自動スケーリング的な簡易処理）
        # （落ち着かないようなら固定のままでも OK）
        v_all = sim.history_v + sim.history_ref
        v_min = min(v_all) - 0.2
        v_max = max(v_all) + 0.2
        ax.set_ylim(v_min, v_max)

        # 描画を更新
        fig.canvas.draw_idle()

    # matplotlib のタイマー機能を使って一定周期で update_sim を呼ぶ
    timer = fig.canvas.new_timer(interval=interval_ms)
    timer.add_callback(update_sim, None)
    timer.start()

    # GUI のメインループ開始
    plt.show()


if __name__ == "__main__":
    main()
