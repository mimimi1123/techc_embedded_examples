class PIDController:
    def __init__(self, kp, ki, kd):
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.prev_error = 0
        self.integral = 0

    def compute(self, target, current, dt):
        error = target - current
        self.integral += error * dt
        derivative = (error - self.prev_error) / dt if dt > 0 else 0
        output = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)
        self.prev_error = error
        return output

# --- 以下テストコード ---
if __name__ == "__main__":
    import time
    
    # ゲイン設定 (テスト用)
    pid = PIDController(kp=1.0, ki=0.1, kd=0.01)
    
    target_val = 100
    current_val = 0
    dt = 0.1
    
    print("PID計算テスト開始 (Target=100)")
    
    # 5ステップだけシミュレーション
    for i in range(5):
        output = pid.compute(target_val, current_val, dt)
        print(f"Step {i+1}: Current={current_val}, Output(PWM)={output:.2f}")
        
        # 簡易的な物理モデル: 出力の10%が次の速度になると仮定
        current_val += output * 0.1