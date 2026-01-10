"""
簡単なモータモデルを用いた PID 速度制御 学習用 GUI プログラム（オフライン版）

【特徴】
・GUI のスライダ／テキスト入力でパラメータ設定
・"Simulate" ボタンでまとめてシミュレーション
・PID が発散してもエラーにならず、描画は ±plot_limit の範囲だけに制限

【必要環境】
pip install matplotlib
"""

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, TextBox, Button


# ===========================================
# モータ＋PID シンプルモデル
# ===========================================

class MotorPIDSim:
    """
    1次遅れモータモデル + PID制御器
      τ * dv/dt + v = K_motor * u

    ・PID発散は許容（クリップなし）
    ・v, u が無限大になっても計算続行
    """

    def __init__(self, dt=0.001, tau=0.2, K_motor=1.0):
        self.dt = dt
        self.tau = tau
        self.K_motor = K_motor

        # 状態
        self.v = 0.0
        self.t = 0.0

        # PID 内部状態
        self.integral = 0.0
        self.prev_error = 0.0

        # ログ
        self.history_t = [0.0]
        self.history_v = [0.0]

    def step(self, setpoint, Kp, Ki, Kd):

        dt = self.dt

        # --- PID 制御 ---
        error = setpoint - self.v
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt

        u = Kp * error + Ki * self.integral + Kd * derivative

        # --- モータ1次遅れ系 ---
        dv = dt * ((-self.v + self.K_motor * u) / self.tau)
        self.v += dv

        # 状態更新
        self.prev_error = error
        self.t += dt

        # 履歴保存
        self.history_t.append(self.t)
        self.history_v.append(self.v)


# ===========================================
# GUI + プロット
# ===========================================

def main():

    # 初期値
    init_Kp = 2.0
    init_Ki = 0.5
    init_Kd = 0.01
    init_setpoint = 1.0
    init_sim_time = 5.0

    # 描画時の制限
    plot_limit = 20.0  # グラフは ±20 の範囲だけ表示

    # GUI の Figure
    fig, ax = plt.subplots()
    plt.subplots_adjust(left=0.1, bottom=0.38)

    # ダミーライン（後で更新）
    t0 = np.array([0, 1])
    v0 = np.array([0, 0])
    sp0 = np.array([init_setpoint, init_setpoint])

    line_v, = ax.plot(t0, v0, label="Motor speed")
    line_sp, = ax.plot(t0, sp0, "--", label="Setpoint")

    ax.set_xlabel("Time [s]")
    ax.set_ylabel("Speed")
    ax.legend(loc="upper right")
    ax.grid(True)
    ax.set_xlim(0, init_sim_time)
    ax.set_ylim(-plot_limit, plot_limit)

    # --------------------------------------
    # スライダ
    # --------------------------------------
    axcolor = "lightgoldenrodyellow"

    ax_Kp = plt.axes([0.1, 0.28, 0.6, 0.03], facecolor=axcolor)
    ax_Ki = plt.axes([0.1, 0.23, 0.6, 0.03], facecolor=axcolor)
    ax_Kd = plt.axes([0.1, 0.18, 0.6, 0.03], facecolor=axcolor)
    ax_sp = plt.axes([0.1, 0.13, 0.6, 0.03], facecolor=axcolor)
    ax_st = plt.axes([0.1, 0.08, 0.6, 0.03], facecolor=axcolor)

    s_Kp = Slider(ax_Kp, "Kp", 0.0, 20.0, valinit=init_Kp)
    s_Ki = Slider(ax_Ki, "Ki", 0.0, 10.0, valinit=init_Ki)
    s_Kd = Slider(ax_Kd, "Kd", 0.0, 5.0, valinit=init_Kd)
    s_sp = Slider(ax_sp, "Setpoint", -2.0, 2.0, valinit=init_setpoint)
    s_st = Slider(ax_st, "SimTime", 0.5, 20.0, valinit=init_sim_time)

    # --------------------------------------
    # テキスト入力欄
    # --------------------------------------
    ax_Kp_box = plt.axes([0.72, 0.28, 0.15, 0.03])
    ax_Ki_box = plt.axes([0.72, 0.23, 0.15, 0.03])
    ax_Kd_box = plt.axes([0.72, 0.18, 0.15, 0.03])
    ax_sp_box = plt.axes([0.72, 0.13, 0.15, 0.03])
    ax_st_box = plt.axes([0.72, 0.08, 0.15, 0.03])

    tb_Kp = TextBox(ax_Kp_box, "", initial=f"{init_Kp}")
    tb_Ki = TextBox(ax_Ki_box, "", initial=f"{init_Ki}")
    tb_Kd = TextBox(ax_Kd_box, "", initial=f"{init_Kd}")
    tb_sp = TextBox(ax_sp_box, "", initial=f"{init_setpoint}")
    tb_st = TextBox(ax_st_box, "", initial=f"{init_sim_time}")

    # TextBox → Slider
    def tb_to_slider(tb, slider, name):
        def _submit(text):
            try:
                val = float(text)
                val = np.clip(val, slider.valmin, slider.valmax)
                slider.set_val(val)
            except Exception:
                print(f"{name}: invalid input")
        return _submit

    tb_Kp.on_submit(tb_to_slider(tb_Kp, s_Kp, "Kp"))
    tb_Ki.on_submit(tb_to_slider(tb_Ki, s_Ki, "Ki"))
    tb_Kd.on_submit(tb_to_slider(tb_Kd, s_Kd, "Kd"))
    tb_sp.on_submit(tb_to_slider(tb_sp, s_sp, "Setpoint"))
    tb_st.on_submit(tb_to_slider(tb_st, s_st, "SimTime"))

    # Slider → TextBox
    def slider_to_tb(slider, tb):
        def _changed(val):
            tb.set_val(f"{val:.3g}")
        return _changed

    s_Kp.on_changed(slider_to_tb(s_Kp, tb_Kp))
    s_Ki.on_changed(slider_to_tb(s_Ki, tb_Ki))
    s_Kd.on_changed(slider_to_tb(s_Kd, tb_Kd))
    s_sp.on_changed(slider_to_tb(s_sp, tb_sp))
    s_st.on_changed(slider_to_tb(s_st, tb_st))

    # --------------------------------------
    # Simulate ボタン
    # --------------------------------------
    ax_button = plt.axes([0.42, 0.01, 0.16, 0.05])
    btn = Button(ax_button, "Simulate", color="lightblue", hovercolor="0.85")

    def run_sim(event):

        Kp = s_Kp.val
        Ki = s_Ki.val
        Kd = s_Kd.val
        sp = s_sp.val
        sim_time = s_st.val

        dt = 0.001
        steps = int(sim_time / dt)

        sim = MotorPIDSim(dt=dt, tau=0.2, K_motor=1.0)

        for _ in range(steps):
            sim.step(sp, Kp, Ki, Kd)

        t = np.array(sim.history_t)
        v = np.array(sim.history_v)

        # NaN / Inf を除去（描画は NaN にして線切れ）
        v_plot = v.copy()
        v_plot[~np.isfinite(v_plot)] = np.nan

        # 描画範囲制限
        v_plot = np.clip(v_plot, -plot_limit, plot_limit)
        sp_plot = np.clip(sp, -plot_limit, plot_limit)

        line_v.set_data(t, v_plot)
        line_sp.set_data(t, np.full_like(t, sp_plot))

        ax.set_xlim(0, sim_time)
        ax.set_ylim(-plot_limit, plot_limit)

        fig.canvas.draw_idle()

    btn.on_clicked(run_sim)

    # 初回実行
    run_sim(None)

    plt.show()


if __name__ == "__main__":
    main()
