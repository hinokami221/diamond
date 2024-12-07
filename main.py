import numpy as np
from generate_mine import generate_mine_field
from all_dynamic import find_max_mining_path, print_mining_path
from greedy import probe_1
from limit_dynamic import probe_with_range
from view import visualize_mine_field


def main():
    layers = 10  # 设置金字塔的层数
    mine_field = generate_mine_field(layers)

    # 使用动态规划计算最大矿产路径
    max_mine_value, dp = find_max_mining_path(mine_field)

    # 打印最大矿产值
    print(f"最大矿产值: {max_mine_value}")

    # 获取最优路径
    dp_path = print_mining_path(dp)
    print(f"最优路径: {dp_path}")

    # 贪心算法
    greedy_path = probe_1(layers, mine_field)

    # 蒙图算法
    probe_with_range(layers + 1, mine_field, 1)

    visualize_mine_field(mine_field[1:, 1:], dp_path, greedy_path)

if __name__ == "__main__":
    main()
