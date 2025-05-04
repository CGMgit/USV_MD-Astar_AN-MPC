import numpy as np


class USVEnv:
    def __init__(self):
        """初始化 USV 运动环境"""
        self.T_sample = 0.1  # 采样时间步长
        self.mass = 500.0  # USV 质量
        self.inertia = 250.0  # 转动惯量
        self.D_u, self.D_v, self.D_omega = 50.0, 30.0, 20.0  # 阻尼系数

        # USV 状态
        self.X, self.Y, self.theta = 0.0, 0.0, 0.0
        self.u, self.v, self.omega = 0.0, 0.0, 0.0

        # 水流状态
        self.V_current = 2.0  # 水流速度
        self.psi_current = np.pi / 4  # 水流方向（45°）

    def update_usv_state(self, T_thrust, T_lateral, tau_yaw):
        """更新 USV 物理状态"""
        # 计算水流影响
        V_body = np.array([
            self.V_current * np.cos(self.psi_current - self.theta),
            self.V_current * np.sin(self.psi_current - self.theta),
            0
        ])
        nu_prime = np.array([self.u, self.v, self.omega]) - V_body

        # 计算惯性、科里奥利和阻尼矩阵
        M = np.array([
            [self.mass, 0, 0],
            [0, self.mass, 0],
            [0, 0, self.inertia]
        ])
        C = np.array([
            [0, 0, -self.mass * self.v],
            [0, 0, self.mass * self.u],
            [self.mass * self.v, -self.mass * self.u, 0]
        ])
        D = np.array([
            [self.D_u, 0, 0],
            [0, self.D_v, 0],
            [0, 0, self.D_omega]
        ])

        # 计算加速度
        tau = np.array([T_thrust, T_lateral, tau_yaw])
        nu_dot = np.linalg.inv(M) @ (tau - C @ np.array([self.u, self.v, self.omega]) - D @ nu_prime)

        # 更新速度
        self.u += nu_dot[0] * self.T_sample
        self.v += nu_dot[1] * self.T_sample
        self.omega += nu_dot[2] * self.T_sample

        # 更新位置
        self.X += (self.u * np.cos(self.theta) - self.v * np.sin(self.theta)) * self.T_sample
        self.Y += (self.u * np.sin(self.theta) + self.v * np.cos(self.theta)) * self.T_sample
        self.theta += self.omega * self.T_sample

    def get_state(self):
        """获取当前状态"""
        return {
            "X": self.X,
            "Y": self.Y,
            "theta": self.theta,
            "u": self.u,
            "v": self.v,
            "omega": self.omega
        }


# ✅ 测试 USV 更新
def test_usv_update():
    """
    测试 USV 物理更新是否正确
    """
    print("🚀 开始 USV 运动仿真测试")

    # 1️⃣ 初始化 USV
    usv = USVEnv()

    # 2️⃣ 施加推力和转动力矩（向前加速 + 逆时针旋转）
    T_thrust = 100.0  # 100 N 推力
    T_lateral = 0.0  # 侧向推力 0
    tau_yaw = 10.0  # 10 Nm 逆时针扭矩

    print(f"初始状态: {usv.get_state()}")

    # 3️⃣ 运行 10 个时间步
    for i in range(10):
        usv.update_usv_state(T_thrust, T_lateral, tau_yaw)
        print(f"Step {i + 1}: {usv.get_state()}")

    # 4️⃣ 结果验证
    final_state = usv.get_state()

    # ✅ 期望的测试结果：
    # - X, Y 位置应该变大（说明前进）
    # - theta 角度应该增加（说明顺时针旋转）
    # - u 速度应该增加（说明加速前进）
    # - omega 角速度应该变大（说明角速度增加）

    assert final_state["X"] > 0, "❌ 测试失败：X 没有正确更新"
    assert final_state["Y"] > 0, "❌ 测试失败：Y 没有正确更新"
    assert final_state["theta"] > 0, "❌ 测试失败：theta 没有正确更新"
    assert final_state["u"] > 0, "❌ 测试失败：u 没有正确更新"
    assert final_state["omega"] > 0, "❌ 测试失败：omega 没有正确更新"

    print("✅ USV 物理更新测试通过！")


# 运行测试
if __name__ == "__main__":
    test_usv_update()
