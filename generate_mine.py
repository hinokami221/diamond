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
    mine_field = np.zeros((layers + 1, layers + 1), dtype=int)

    # 为每个位置生成一个矿产值
    for i in range(1, layers + 1):
        for j in range(1, layers - i + 2):  # 只在左上三角区域内生成矿产
            mine_field[i, j] = np.random.uniform(50, 1000)

    print(mine_field)

    return mine_field
