import numpy as np


def find_max_mining_path(mine_field):
    """
    通过动态规划计算从金字塔顶到底的最大矿产路径。

    参数:
    mine_field -- 矿产分布图（左上三角矩阵）

    返回:
    max_mine_value -- 最大矿产值
    dp -- 动态规划表
    """
    layers = mine_field.shape[0]

    # 创建一个DP表，dp[i][j]表示到达位置(i, j)的最大矿产值
    dp = np.zeros((layers, layers), dtype=int)

    # 填充dp表
    for i in range(1, layers):
        for j in range(1, layers - i + 1):
            dp[i, j] = mine_field[i, j] + max(dp[i - 1, j], dp[i, j - 1])  # 可以从上方或左方过来

    max_mine_value = 0

    for i in range(1, layers):
        for j in range(1, layers - i + 1):
            tmp = dp[i][j]
            if tmp > max_mine_value:
                max_mine_value = tmp

    return max_mine_value, dp


def print_mining_path(dp):
    """
    回溯动态规划表，输出最优路径。

    参数:
    dp -- 动态规划表

    返回:
    path -- 最优路径
    """
    layers = dp.shape[0]
    path = []
    max_mine_value = 0
    max_i = 0
    max_j = 0
    # 在最后一层（数组副对角线）中找到最大值的位置
    for i in range(1, layers):
        for j in range(1, layers - i + 1):
            tmp = dp[i][j]
            if tmp > max_mine_value:
                max_mine_value = tmp
                max_i = i
                max_j = j

    path.append((max_i - 1, max_j - 1))


    while max_i > 0:
        if max_i > 1 and max_j > 0 and dp[max_i - 1, max_j] >= dp[max_i, max_j - 1]:
            max_i -= 1  # 从上方过来
        elif max_i > 0 and max_j > 1 and dp[max_i, max_j - 1] >= dp[max_i - 1, max_j]:
            max_j -= 1  # 从左边过来
        elif max_i == 1 and max_j == 1:
            break
        path.append((max_i - 1, max_j - 1))

    # 反转路径，使得路径从起点到终点
    return path[::-1]
