import matplotlib.pyplot as plt
import numpy as np

# 设置中文字体
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

# 港口/地区
ports = {
    "葵青货柜码头": (22.33465, 114.12268),
    "西区公用码头": (22.28833, 114.13152),
    "西区公用货物装卸区": (22.28165, 114.11927),
    "中环码头": (22.28788, 114.15885),
    "尖沙咀码头": (22.29372, 114.16808),
    "观塘码头": (22.31200, 114.22600),  # 观塘码头
    "红磡码头": (22.30047, 114.19501)   # 新增
}

# 避风塘
typhoon_shelters = {
    "油麻地避风塘": (22.31038, 114.15698),
    "昂船洲避风塘": (22.31200, 114.13500),
    "九龙湾避风塘": (22.30300, 114.11500),
    "北角避风塘": (22.31000, 114.12700),
    "青衣避风塘": (22.30500, 114.15000),
    "香港仔避风塘": (22.29900, 114.11800),
    "铜锣湾避风塘": (22.28250, 114.18750),
    "鲤鱼门避风塘": (22.29500, 114.23800)  # 鲤鱼门避风塘
}

# 锚地
anchorages = {
    "西部检疫及入境锚地": (22.30762, 114.10332),
    "西部危险品锚地": (22.31340, 114.11392),
    "基列特 3 号": (22.30625, 114.13038),
    "基列特 2 号": (22.30155, 114.12385),
    "基列特 1 号": (22.29885, 114.10535),
    "东部锚地": (22.28000, 114.25000),  # 新增
    "中部锚地": (22.29000, 114.21000)   # 新增
}

# 障碍物区域（四边形）
obstacles = {
    "青衣": [(22.33928, 114.08805), (22.32630, 114.09095), (22.33123, 114.11768), (22.34352, 114.11328)],
    "7号货柜码头": [(22.33543, 114.12375), (22.33698, 114.12972), (22.32847, 114.12660), (22.33068, 114.13388)],
    "昂船洲": [(22.32318, 114.12230), (22.31885, 114.12933), (22.31718, 114.14320), (22.32307, 114.14653)],

    # 新增障碍物（四边形格式）
    "青洲": [(22.29050, 114.13020), (22.28950, 114.13150), (22.28890, 114.13080), (22.28980, 114.12990)],
    "东博寮海峡小岛": [(22.28330, 114.24970), (22.28370, 114.25050), (22.28270, 114.25070), (22.28250, 114.24980)],
    "政府船只维修码头": [(22.31230, 114.14290), (22.31270, 114.14350), (22.31210, 114.14370), (22.31180, 114.14320)],
    "香港国际邮轮码头": [(22.30200, 114.19270), (22.30240, 114.19330), (22.30160, 114.19350), (22.30120, 114.19290)],
    "昂船洲大桥": [(22.31640, 114.13290), (22.31690, 114.13360), (22.31610, 114.13380), (22.31570, 114.13310)],
    "西九龙高架桥": [(22.31010, 114.15960), (22.31050, 114.16040), (22.30950, 114.16060), (22.30910, 114.15980)],
    "香港中区油库": [(22.28490, 114.15460), (22.28530, 114.15540), (22.28450, 114.15560), (22.28410, 114.15480)],
    "昂船洲军用码头": [(22.31800, 114.13960), (22.31840, 114.14040), (22.31760, 114.14060), (22.31720, 114.13980)],
    "香港国际机场水域": [(22.30800, 113.99980), (22.30840, 114.00060), (22.30760, 114.00080), (22.30720, 114.00000)],
    "昂船洲军事禁区水域": [(22.32190, 114.13260), (22.32230, 114.13340), (22.32150, 114.13360), (22.32110, 114.13280)],
    "油麻地避风塘渔船区": [(22.30990, 114.15710), (22.31030, 114.15790), (22.30950, 114.15810), (22.30910, 114.15730)],
    "香港仔避风塘渔船区": [(22.29910, 114.11960), (22.29950, 114.12040), (22.29870, 114.12060), (22.29830, 114.11980)],
    "九龙边界": [
        (22.31815, 114.15420), (22.28712, 114.17587),
        (22.29633, 114.19795), (22.30300, 114.19278),
        (22.30638, 114.18612), (22.30747, 114.18247),
        (22.31118, 114.18112), (22.31815, 114.15420)
    ],
    "香港北角边界": [
        (22.28453, 114.18223), (22.29343, 114.20122),
        (22.28875, 114.21612), (22.28267, 114.23058)
    ],
    "香港石塘咀边界": [
        (22.28032, 114.11953), (22.28687, 114.13240),
        (22.28967, 114.14628), (22.28272, 114.16623),
        (22.28225, 114.17448)
    ]
}

# 最优路径
optimal_path = [
    ("观塘码头", "鲤鱼门避风塘"),
    ("鲤鱼门避风塘", "九龙湾避风塘"),
    ("九龙湾避风塘", "西部检疫及入境锚地"),
    ("西部检疫及入境锚地", "葵青货柜码头")
]

# 绘制地图
def plot_map():
    plt.figure(figsize=(12, 10))

    # 取消科学计数法
    plt.ticklabel_format(style='plain', axis='both')

    # 设置地图范围
    plt.xlim(114.08, 114.26)
    plt.ylim(22.28, 22.35)

    # 绘制港口/地区
    for name, (lat, lon) in ports.items():
        plt.scatter(lon, lat, c='blue', marker='o', label='港口/地区' if name == list(ports.keys())[0] else "")
        plt.annotate(name, xy=(lon, lat), xytext=(lon + 0.005, lat + 0.002), fontsize=9,
                     arrowprops=dict(facecolor='blue', arrowstyle='->'),
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # 绘制避风塘
    for name, (lat, lon) in typhoon_shelters.items():
        plt.scatter(lon, lat, c='green', marker='s', label='避风塘' if name == list(typhoon_shelters.keys())[0] else "")
        plt.annotate(name, xy=(lon, lat), xytext=(lon + 0.005, lat + 0.002), fontsize=9,
                     arrowprops=dict(facecolor='green', arrowstyle='->'),
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # 绘制锚地
    for name, (lat, lon) in anchorages.items():
        plt.scatter(lon, lat, c='orange', marker='^', label='锚地' if name == list(anchorages.keys())[0] else "")
        plt.annotate(name, xy=(lon, lat), xytext=(lon + 0.005, lat + 0.002), fontsize=9,
                     arrowprops=dict(facecolor='orange', arrowstyle='->'),
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))

    # 绘制障碍物区域（红色多边形）并添加图例
    for name, points in obstacles.items():
        latitudes, longitudes = zip(*points)
        latitudes += (latitudes[0],)  # 闭合多边形
        longitudes += (longitudes[0],)

        plt.plot(longitudes, latitudes, linestyle='solid', color='red', alpha=0.7, linewidth=2)
        plt.fill(longitudes, latitudes, color='red', alpha=0.3)

        # 计算障碍物中心点并添加注释
        center_lat, center_lon = np.mean(latitudes), np.mean(longitudes)
        plt.annotate(name, xy=(center_lon, center_lat), xytext=(center_lon + 0.005, center_lat + 0.002),
                     fontsize=9, arrowprops=dict(facecolor='red', arrowstyle='->'),
                     bbox=dict(facecolor='white', alpha=0.7, edgecolor='none'))
    # 在图例中补充一个红色障碍物区域图例项
    plt.scatter([], [], color='red', label='障碍物区域')

    # 绘制最优路径
    for start, end in optimal_path:
        lat1, lon1 = ports.get(start, typhoon_shelters.get(start, anchorages.get(start)))
        lat2, lon2 = ports.get(end, typhoon_shelters.get(end, anchorages.get(end)))
        plt.plot([lon1, lon2], [lat1, lat2], color='green', linewidth=3, label='最优路径' if start == optimal_path[0][0] else "")

    # 设置图例
    plt.legend()
    # 设置标题和标签
    plt.title("从观塘码头到葵青货柜码头的最优路径")
    plt.xlabel("经度")
    plt.ylabel("纬度")
    plt.grid(True)

    # 显示地图
    plt.show()

# 运行地图绘制
plot_map()
