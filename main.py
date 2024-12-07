from generate_mine import generate_mine_field
from all_dynamic import find_max_mining_path, print_mining_path
from greedy import probe_1
from limit_dynamic import probe_m
from view import visualize_mine_field


def main():
    layers = int(input("请输入矿产分布层数 (layers): "))
    mine_field = generate_mine_field(layers)

    # 使用动态规划计算最大矿产路径
    dp = find_max_mining_path(mine_field)

    # 获取最优路径
    dp_path = print_mining_path(dp)
    print(f"最优路径: {dp_path}")

    # 贪心算法
    greedy_path = probe_1(layers, mine_field)

    steps = int(input("请输入蒙图算法预测的步数 (steps): "))
    # 蒙图算法
    mask_path = probe_m(layers + 1, mine_field, steps)

    visualize_mine_field(mine_field[1:, 1:], dp_path, greedy_path)

if __name__ == "__main__":
    main()