from 科研代码.宏观路径地图数据处理 import calculate_min_perimeter_cut

# ✅ 测试数据（严格独立）
test_points = {
    "A": (0, 0),
    "B": (1, 1)
}

test_obstacles = {
    "正方形障碍物": [(0, 0), (1, 0), (1, 1), (0, 1)]
}

test_connections = [("A", "B")]

# ✅ 确保 `calculate_min_perimeter_cut()` 仅运行测试数据
test_results = calculate_min_perimeter_cut(test_points, test_connections, test_obstacles)

# ✅ 只打印 **测试数据** 的结果，避免地图数据干扰
for edge, (perimeter, crossed_obstacles) in test_results.items():
    obstacles_str = ", ".join(crossed_obstacles) if crossed_obstacles else "无"
    print(f"🛠️ 测试边 {edge}: 最小环绕周长 = {perimeter:.2f}，穿越障碍物: {obstacles_str}")

# ✅ 断言检查（失败时输出详细调试信息）
expected_perimeter = 2.00
actual_perimeter = round(test_results[("A", "B")][0], 2)

if actual_perimeter != expected_perimeter:
    print("❌ 测试失败！")
    print(f"❌ 预期周长 = {expected_perimeter:.2f}，但计算得到 = {actual_perimeter:.2f}")
    print(f"❌ 穿越障碍物: {test_results[('A', 'B')][1]}")
    raise AssertionError("❌ 测试失败：最小环绕周长计算错误！")

print("✅ 测试通过！")
