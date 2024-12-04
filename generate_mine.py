import numpy as np


def generate_mine_field(layers: int):
    """
    生成金字塔形状的矿产分布图，矿产值只生成在左上三角区域。

    参数:
    layers -- 金字塔的层数

    返回:
    mine_field -- 矿产分布图（二维数组）
    """
    np.random.seed(42)  # 保证结果复现
    mine_field = np.zeros((layers, layers), dtype=int)

    # 为每个位置生成一个矿产值
    for i in range(0, layers):
        for j in range(0, layers - i):  # 只在左上三角区域内生成矿产
            mine_field[i, j] = np.random.normal(loc=50, scale=10)

    print(mine_field)

    return mine_field
