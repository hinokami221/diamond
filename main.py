import numpy as np
from generate_mine import generate_mine_field
from min_alg import find_max_mining_path, print_mining_path
from plot_mine import plot_mine_field, plot_optimal_path

def main():
    layers = 5  # 设置金字塔的层数
    mine_field = generate_mine_field(layers)

    # 绘制矿产分布图
    plot_mine_field(mine_field)

    # 使用动态规划计算最大矿产路径
    max_mine_value, dp = find_max_mining_path(mine_field)
    print(dp)
    # 打印最大矿产值
    print(f"最大矿产值: {max_mine_value}")

    # 获取最优路径
    path = print_mining_path(dp)
    print(f"最优路径: {path}")

    # 绘制最优路径的矿产分布图
    plot_optimal_path(mine_field, path)

if __name__ == "__main__":
    main()
