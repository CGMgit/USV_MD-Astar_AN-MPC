import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

# ---------------- 1️⃣ 解决 Matplotlib 中文显示问题 ----------------
plt.rcParams['font.sans-serif'] = ['SimHei']  # 设置字体为黑体，支持中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

# ---------------- 2️⃣ 定义系统参数（常量） ----------------
m = 500.0  # 质量 (kg)
I_z = 250.0  # 转动惯量 (kg·m²)
D_u = 4.0  # 纵向阻尼 (Ns/m)
D_v = 15.0  # 横向阻尼 (Ns/m)
D_omega = 3.0  # 角阻尼 (Ns/rad)
delta_t = 0.1  # 时间步长 (s)
sim_time = 10  # 总仿真时间 (s)

# ---------------- 3️⃣ 定义USV状态变量（系统变量） ----------------
X, Y, theta = 0.0, 0.0, 0.0  # 位置 (m) 和航向角 (rad)
u, v, omega = 0.0, 0.0, 0.0  # 速度 (m/s, rad/s)

# 存储轨迹数据
trajectory = {
    "time": [],
    "X": [],
    "Y": [],
    "theta": [],
    "u": [],
    "v": [],
    "omega": []
}

# ---------------- 4️⃣ 定义动力学更新函数 ----------------
def update_usv_state(_T_thrust, _T_lateral, _tau_yaw, _V_current, _psi_current):
    global X, Y, theta, u, v, omega

    # 计算水流影响
    V_body = np.array([
        V_current * np.cos(psi_current - theta),
        V_current * np.sin(psi_current - theta),
        0
    ])
    nu_prime = np.array([u, v, omega]) - V_body

    # 计算惯性、科里奥利和阻尼矩阵
    M = np.array([[m, 0, 0], [0, m, 0], [0, 0, I_z]])
    C = np.array([[0, 0, -m * v], [0, 0, m * u], [m * v, -m * u, 0]])
    D = np.array([[D_u, 0, 0], [0, D_v, 0], [0, 0, D_omega]])

    # 计算加速度
    tau = np.array([T_thrust, T_lateral, tau_yaw])
    nu_dot = np.linalg.inv(M) @ (tau - C @ np.array([u, v, omega]) - D @ nu_prime)

    # 更新速度
    u += nu_dot[0] * delta_t
    v += nu_dot[1] * delta_t
    omega += nu_dot[2] * delta_t

    # 更新位置
    X += (u * np.cos(theta) - v * np.sin(theta)) * delta_t
    Y += (u * np.sin(theta) + v * np.cos(theta)) * delta_t
    theta += omega * delta_t

    # 记录数据
    trajectory["time"].append(len(trajectory["time"]) * delta_t)
    trajectory["X"].append(X)
    trajectory["Y"].append(Y)
    trajectory["theta"].append(theta)
    trajectory["u"].append(u)
    trajectory["v"].append(v)
    trajectory["omega"].append(omega)

# ---------------- 5️⃣ 运行仿真 ----------------
# 设置控制输入
T_thrust = 500.0  # 推力 (N)
T_lateral = 50.0  # 侧向推力 (N)
tau_yaw = 20.0  # 旋转力矩 (Nm)
V_current = 2.0  # 水流速度 (m/s)
psi_current = np.pi / 4  # 水流方向 (rad)

# 运行仿真
for _ in range(int(sim_time / delta_t)):
    update_usv_state(T_thrust, T_lateral, tau_yaw, V_current, psi_current)

# ---------------- 6️⃣ 结果可视化 ----------------
fig, ax = plt.subplots()
ax.plot(trajectory["X"], trajectory["Y"], label="USV 轨迹", marker="o")
ax.set_xlabel("X 位置 (m)")
ax.set_ylabel("Y 位置 (m)")
ax.set_title("USV 运动轨迹")
ax.legend()
ax.grid()

# 显示图表
plt.show()

# ---------------- 7️⃣ 输出仿真数据 ----------------
df = pd.DataFrame(trajectory)
print(df)  # 直接打印数据
df.to_csv("usv_data.csv", index=False)  # 保存到 CSV 文件
