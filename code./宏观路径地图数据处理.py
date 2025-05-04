import numpy as np
import pandas as pd
from shapely.ops import split
from shapely.geometry import GeometryCollection

# 位置转化为 X-Y 坐标数据
defined_points = {
    "葵青货柜码头": (12622.956, 6076.803),
    "西区公用码头": (13532.533, 926.254),
    "西区公用货物装卸区": (12272.090, 183.472),
    "中环码头": (16344.608, 876.216),
    "尖沙咀码头": (17294.314, 1525.594),
    "观塘码头": (23253.897, 3558.238),
    "红磡码头": (18417.909, 2279.496),
    "油麻地避风塘": (16152.198, 3378.102),
    "昂船洲避风塘": (13890.602, 3558.238),
    "九龙湾避风塘": (11832.735, 2557.483),
    "北角避风塘": (13067.455, 3335.848),
    "青衣避风塘": (15434.002, 2779.873),
    "香港仔避风塘": (12141.415, 2112.704),
    "铜锣湾避风塘": (19292.503, 277.987),
    "鲤鱼门避风塘": (24488.617, 1667.924),
    "西部检疫及入境锚地": (10630.941, 3071.204),
    "西部危险品锚地": (11721.610, 3713.911),
    "基列特 3 号": (13415.235, 2918.867),
    "基列特 2 号": (12743.341, 2396.251),
    "基列特 1 号": (10839.814, 2096.024),
    "东部锚地": (25723.337, 0.0),
    "中部锚地": (21607.603, 1111.949)
}

# 障碍物数据
defined_obstacles = {
    "青衣": [(9059.759, 6591.635), (9358.15, 5148.325), (12108.489, 5696.516), (11655.759, 7063.102)],
    "7号货柜码头": [(12733.052, 6163.535), (13347.325, 6335.887), (13026.298, 5389.618), (13775.362, 5635.359)],
    "昂船洲": [(12583.857, 4801.397), (13307.197, 4319.923), (14734.328, 4134.227), (15076.962, 4789.165)],
    "青洲": [(13396.714, 1167.547), (13530.475, 1056.352), (13458.45, 989.635), (13365.846, 1089.71)],
    "东博寮海峡小岛": [(25692.469, 366.943), (25774.784, 411.421), (25795.363, 300.226), (25702.759, 277.987)],
    "政府船只维修码头": [(14703.46, 3591.596), (14765.196, 3636.074), (14785.774, 3569.357), (14734.328, 3535.999)],
    "香港国际邮轮码头": [(19827.548, 2446.288), (19889.284, 2490.766), (19909.863, 2401.81), (19848.127, 2357.332)],
    "昂船洲大桥": [(13674.526, 4047.495), (13746.551, 4103.093), (13767.13, 4014.137), (13695.105, 3969.659)],
    "西九龙高架桥": [(16421.778, 3346.967), (16504.093, 3391.445), (16524.672, 3280.25), (16442.357, 3235.772)],
    "香港中区油库": [(15907.312, 544.855), (15989.626, 589.333), (16010.205, 500.377), (15927.89, 455.899)],
    "昂船洲军用码头": [(14363.911, 4225.407), (14446.226, 4269.885), (14466.805, 4180.929), (14384.49, 4136.451)],
    "香港国际机场水域": [(-20.579, 3113.458), (61.736, 3157.936), (82.315, 3068.98), (0.0, 3024.502)],
    "昂船洲军事禁区水域": [(13643.658, 4659.067), (13725.973, 4703.545), (13746.551, 4614.589), (13664.237, 4570.111)],
    "油麻地避风塘渔船区": [(16164.545, 3324.728), (16246.86, 3369.206), (16267.438, 3280.25), (16185.124, 3235.772)],
    "香港仔避风塘渔船区": [(12306.045, 2123.823), (12388.359, 2168.301), (12408.938, 2079.345), (12326.623, 2034.867)],
    "九龙边界": [(15866.154, 4242.086), (18095.853, 791.708), (20367.738, 1815.813), (19835.78, 2557.483), (19150.51, 2933.322), (18774.949, 3054.525), (18636.043, 3467.058), (15866.154, 4242.086)],
    "香港北角边界": [(18750.255, 503.713), (20704.2, 1493.348), (22237.311, 972.956), (23725.148, 296.89)],
    "香港石塘咀边界": [(12298.842, 35.582), (13623.079, 763.909), (15051.239, 1075.255), (17103.961, 302.45), (17952.832, 250.189)]
}

# 连接关系
defined_connections = [
    ("中环码头", "铜锣湾避风塘"),
    ("尖沙咀码头", "油麻地避风塘"),
    ("观塘码头", "鲤鱼门避风塘"),
    ("红磡码头", "九龙湾避风塘"),
    ("葵青货柜码头", "青衣避风塘"),
    ("油麻地避风塘", "昂船洲避风塘"),
    ("九龙湾避风塘", "鲤鱼门避风塘"),
    ("铜锣湾避风塘", "北角避风塘"),
    ("鲤鱼门避风塘", "东部锚地"),
    ("九龙湾避风塘", "昂船洲避风塘"),
    ("油麻地避风塘", "北角避风塘"),
    ("青衣避风塘", "昂船洲避风塘"),
    ("北角避风塘", "昂船洲避风塘"),
    ("北角避风塘", "油麻地避风塘"),
    ("鲤鱼门避风塘", "九龙湾避风塘"),
    ("油麻地避风塘", "西部检疫及入境锚地"),
    ("鲤鱼门避风塘", "东部锚地"),
    ("九龙湾避风塘", "基列特 1 号"),
    ("九龙湾避风塘", "中部锚地"),
    ("青衣避风塘", "基列特 3 号"),
    ("铜锣湾避风塘", "基列特 2 号"),
    ("九龙湾避风塘", "西部检疫及入境锚地"),
    ("东部锚地", "基列特 1 号"),
    ("西部检疫及入境锚地", "西部危险品锚地"),
    ("西部检疫及入境锚地", "基列特 3 号"),
    ("东部锚地", "中部锚地"),
    ("基列特 3 号", "基列特 2 号"),
    ("基列特 2 号", "基列特 1 号"),
    ("西部危险品锚地", "基列特 1 号"),
    ("中部锚地", "基列特 2 号"),
    ("西部危险品锚地", "基列特 3 号"),
    ("西部检疫及入境锚地", "中环码头"),
    ("东部锚地", "观塘码头"),
    ("基列特 1 号", "红磡码头"),
    ("基列特 3 号", "尖沙咀码头"),
    ("观塘码头", "中部锚地"),
    ("西区公用码头", "西部检疫及入境锚地"),
    ("西区公用货物装卸区", "基列特 3 号"),
    ("葵青货柜码头", "西部检疫及入境锚地"),
    ("尖沙咀码头", "基列特 2 号")
]

# 计算边的欧几里得距离
def calculate_edge_distances(points, connections):
    """
    计算每条边的欧几里得距离。

    参数：
    - points: dict[str, tuple(float, float)] 地点名称 -> (X, Y) 坐标
    - connections: list[tuple(str, str)] 连接关系列表

    返回：
    - edge_distances: dict[tuple(str, str), float] 记录每条边的欧几里得距离
    """
    edge_distances1 = {}
    for start, end in connections:
        x1, y1 = points[start]
        x2, y2 = points[end]
        distance1 = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
        edge_distances1[(start, end)] = distance1
    return edge_distances1

# 计算所有边的欧几里得距离
edge_distances = calculate_edge_distances(defined_points, defined_connections)


def validate_obstacles(obstacles):
    """
    预处理障碍物，确保所有多边形是有效的。

    参数：
    - obstacles: dict[str, list[tuple(float, float)]] 障碍物名称 -> 多边形点集

    返回：
    - valid_obstacles: dict[str, Polygon] 经过修正的障碍物
    """
    valid_obstacles = {}
    for name, points in obstacles.items():
        polygon = Polygon(points)

        # 检查障碍物是否有效
        if not polygon.is_valid:
            print(f"⚠️ 障碍物 {name} 发现无效几何结构，尝试修复...")
            polygon = polygon.buffer(0)  # 自动修正

        if polygon.is_valid:
            valid_obstacles[name] = polygon
        else:
            print(f"❌ 障碍物 {name} 仍然无效，可能需要手动检查！")

    return valid_obstacles


def calculate_min_perimeter_cut(points, connections, obstacles):
    """
    计算路径穿越障碍物的最小周长，并减去交集长度，同时记录穿越的障碍物名称。

    参数：
    - points: dict[str, tuple(float, float)] 地点名称 -> (X, Y) 坐标
    - connections: list[tuple(str, str)] 连接关系列表
    - obstacles: dict[str, list[tuple(float, float)]] 障碍物名称 -> 多边形点集

    返回：
    - min_perimeters: dict[tuple(str, str), tuple(float, list[str])]
      - 键: (起点, 终点)
      - 值: (路径穿越的最小周长, 穿越的障碍物列表)
    """
    min_perimeters = {}

    for start, end in connections:
        x1, y1 = points[start]
        x2, y2 = points[end]
        path_line = LineString([(x1, y1), (x2, y2)])

        total_min_perimeter = 0
        crossed_obstacles1 = []

        for obs_name, obstacle in obstacles.items():
            polygon = Polygon(obstacle)

            # 修复拓扑错误
            if not polygon.is_valid:
                polygon = polygon.buffer(0.1)

            try:
                intersection = path_line.intersection(polygon)
                if not intersection.is_empty:
                    crossed_obstacles1.append(obs_name)  # 记录穿越的障碍物名称

                    # ✅ 使用 `split()` 直接分割成两个多边形
                    cut_polygons = split(polygon, path_line)

                    if isinstance(cut_polygons, GeometryCollection):
                        perimeters = [geom.length for geom in cut_polygons.geoms if isinstance(geom, Polygon)]
                    elif isinstance(cut_polygons, Polygon):
                        perimeters = [cut_polygons.length]
                    else:
                        perimeters = []

                    # ✅ 选取周长最小的多边形
                    min_perimeter = min(perimeters) if perimeters else polygon.length

                    # ✅ 计算最终路径长度
                    adjusted_perimeter = max(min_perimeter - intersection.length, 0)
                    total_min_perimeter += adjusted_perimeter

                    # 🔍 Debug 输出，检查计算过程
                    print(
                        f"调试: 边 ({start}, {end}) 穿越 {obs_name}，最小周长 = {min_perimeter:.4f}，交点长度 = {intersection.length:.4f}，最终调整值 = {adjusted_perimeter:.4f}")

            except Exception as e:
                print(f"⚠️ 计算边 {start} -> {end} 时发生错误: {e}")
                continue

        min_perimeters[(start, end)] = (total_min_perimeter, crossed_obstacles1)

    return min_perimeters

from shapely.geometry import LineString, Polygon

def calculate_crossing_lengths(points, connections, obstacles):
    """
    计算每条边穿越障碍物的总交点长度（穿越长度）。

    参数：
    - points: dict[str, tuple(float, float)] 地点名称 -> (X, Y) 坐标
    - connections: list[tuple(str, str)] 连接关系列表
    - obstacles: dict[str, list[tuple(float, float)]] 障碍物名称 -> 多边形点集

    返回：
    - crossing_lengths: dict[tuple(str, str), float]
      - 键: (起点, 终点)
      - 值: 该边穿越所有障碍物的总交点长度
    """
    crossing_lengths1 = {}

    for start, end in connections:
        x1, y1 = points[start]
        x2, y2 = points[end]
        path_line = LineString([(x1, y1), (x2, y2)])

        total_crossing_length = 0

        for obs_name, obstacle in obstacles.items():
            polygon = Polygon(obstacle)

            if not polygon.is_valid:
                polygon = polygon.buffer(0)

            try:
                intersection = path_line.intersection(polygon)
                if not intersection.is_empty:
                    total_crossing_length += intersection.length

            except Exception as e:
                print(f"⚠️ 计算边 {start} -> {end} 穿越长度时发生错误: {e}")
                continue

        crossing_lengths1[(start, end)] = total_crossing_length

    return crossing_lengths1

# 1️⃣ 预处理障碍物数据，确保所有障碍物是有效的
validated_obstacles = validate_obstacles(defined_obstacles)

# 输出欧几里得距离
print("\n🔹 欧几里得距离计算结果:")
for edge, distance in edge_distances.items():
    print(f"边 {edge}: 欧几里得距离 = {distance:.2f} 米")

# 计算所有边穿越障碍物的环绕周长
obstacle_min_perimeters = calculate_min_perimeter_cut(defined_points, defined_connections, defined_obstacles)

# 输出结果，增加穿越障碍物信息
for edge, (perimeter, crossed_obstacles) in obstacle_min_perimeters.items():
    obstacles_str = ", ".join(crossed_obstacles) if crossed_obstacles else "无"
    print(f"边 {edge}: 穿越障碍物的最小环绕周长 = {perimeter:.2f} 米，穿越障碍物: {obstacles_str}")

# 计算所有边穿越障碍物的交点总长度
crossing_lengths = calculate_crossing_lengths(defined_points, defined_connections, defined_obstacles)

# 输出结果，增加穿越障碍物交点总长度信息
print("\n🔹 穿越障碍物的交点总长度计算结果:")
for edge, crossing_length in crossing_lengths.items():
    print(f"边 {edge}: 穿越障碍物交点总长度 = {crossing_length:.2f} 米")

# 参数设定（严格遵循你的公式）
MU = 1.0         # 穿越交点总长度权重因子
LAMBDA = 1.2     # 障碍物绕行距离权重因子

# 计算最终边的权重（严格版）
edge_weights = []
for edge, euclidean_distance in edge_distances.items():
    obstacle_distance, crossed_obstacles = obstacle_min_perimeters.get(edge, (0, []))
    crossing_length = crossing_lengths.get(edge, 0)

    # ✅ 严格按照你的公式进行权重修正
    adjusted_distance = max(euclidean_distance - MU * crossing_length, 0)
    total_weight = adjusted_distance + (LAMBDA * obstacle_distance)

    edge_weights.append([
        edge[0], edge[1],
        round(euclidean_distance, 2),
        round(crossing_length, 2),
        round(obstacle_distance, 2),
        round(total_weight, 2),
        ", ".join(crossed_obstacles) if crossed_obstacles else "无"
    ])

# 创建 DataFrame 并保存为 CSV（✅ 新增穿越交点长度这一列）
df = pd.DataFrame(edge_weights,
                  columns=["起点", "终点", "欧几里得距离 (m)", "穿越交点总长度 (m)", "障碍物绕行距离 (m)", "最终权重 (m)", "穿越障碍物"])
csv_filename = "edge_weights.csv"
df.to_csv(csv_filename, index=False, encoding="utf-8-sig")

print(f"✅ 新数据已保存至 {csv_filename}")















'''
此处存在的代码为在研究过程中，已经实现，但是由于研究需要，改变研究方法而导致废弃的代码
方法1：计算与障碍物区域相交的直线距离
def calculate_obstacle_cross_length(points, connections, obstacles):
    """
    计算所有边穿越障碍物的总长度。

    参数：
    - points: dict[str, tuple(float, float)] 地点名称 -> (X, Y) 坐标
    - connections: list[tuple(str, str)] 连接关系列表
    - obstacles: dict[str, Polygon] 经过验证的障碍物

    返回：
    - cross_lengths: dict[tuple(str, str), float] 记录每条边穿越障碍物的总长度
    """
    cross_lengths = {}

    for start, end in connections:
        x1, y1 = points[start]
        x2, y2 = points[end]
        path_line = LineString([(x1, y1), (x2, y2)])
        total_cross_length = 0

        for obs_name, polygon in obstacles.items():
            try:
                intersection = path_line.intersection(polygon)
                if not intersection.is_empty:
                    total_cross_length += intersection.length
            except Exception as e:
                print(f"⚠️ 计算边 {start} -> {end} 时发生错误: {e}")
                print(f"问题发生在障碍物: {obs_name}，坐标: {polygon}")
                continue

        cross_lengths[(start, end)] = total_cross_length

    return cross_lengths
    
    #  计算所有边穿越障碍物的长度
obstacle_cross_lengths = calculate_obstacle_cross_length(defined_points, defined_connections, validated_obstacles)
'''























































