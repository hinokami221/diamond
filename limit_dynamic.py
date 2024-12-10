import random
from all_dynamic import find_max_mining_path, print_mining_path

# 探测器
def dynamic(x, y, steps, n, mine_field):
    """
    动态规划计算在当前坐标 (x, y) 位置下，最多走 `steps` 步的最大收益
    """
    # 初始化动态规划表格 arr，大小应为 n + 1，以避免越界
    arr = [[0] * (n + steps + 1) for _ in range(n + steps + 1)]  # 动态规划表格的大小为 n + steps +1

    res = 0
    if steps < 0:
        return 0

    # 如果步数为0时，直接返回当前位置的矿产值
    if steps == 0:
        return mine_field[x][y]

    # 计算从 (x, y) 出发，最多走 `steps` 步的最大值
    if x + steps + y > n:  # 检查 x + steps 是否越界
        steps = n - x - y  # 限制最大步数

    # 遍历计算每个位置的最大值，动态规划从上方或左方来
    for i in range(x, min(x + steps, n) + 1):  # 限制 i 不超出 n
        for j in range(y, x + steps + 1):  # 限制 j 不超出 n
            if i == x and j == y:
                arr[i][j] = mine_field[i][j]  # 起始位置的值
            elif i == x:
                arr[i][j] = arr[i][j - 1] + mine_field[i][j]  # 向右移动
            elif j == y:
                arr[i][j] = arr[i - 1][j] + mine_field[i][j]  # 向下移动
            else:
                arr[i][j] = max(arr[i - 1][j], arr[i][j - 1]) + mine_field[i][j]  # 上下两种路径的最大值

    # 找到最终步数范围内的最大值
    for i in range(x, min(x + steps, n) + 1):  # 限制 i 不超出 n
        if y + steps + x - i <= n:  # 防止越界
            res = max(res, arr[i][y + steps + x - i])

    return res


def probe_go(x, y, res, m, n, mine_field, path):
    """
    递归预测矿工接下来的行动方向，通过选择最大期望值的路径
    """
    if m == 0 or x > n or y > n:  # 如果步数为0或越界，终止递归
        return res, path

    # 当前状态的最大收益
    a = b = 0

    # 计算当前可走的步数
    max_steps_right = n - x
    max_steps_down = n - y
    steps_possible = min(m, max_steps_right, max_steps_down)

    # 向右走
    if x + 1 <= n and y <= n and x + y + 1 <= n + 1:
        a = dynamic(x + 1, y, steps_possible - 1, n, mine_field)

    # 向下走
    if x <= n and y + 1 <= n and x + y + 1 <= n + 1:
        b = dynamic(x, y + 1, steps_possible - 1, n, mine_field)

    # 如果两个方向都不可行，则直接返回当前结果
    if a == 0 and b == 0:
        return res, path

    # 根据两个方向的预期收益，选择最优路径
    if a > b:
        res += mine_field[x + 1][y]
        path.append((x + 1, y))
        return probe_go(x + 1, y, res, m - 1, n, mine_field, path) # 已经走了一步，step - 1
    else:
        res += mine_field[x][y + 1]
        path.append((x, y + 1))
        return probe_go(x, y + 1, res, m - 1, n, mine_field, path)


def probe_m(n, mine_field, m):
    """
    主函数，预测矿工从位置 (1, 1) 开始，走 m 步的最大可能收益
    """
    res = mine_field[1][1]  # 初始位置的值
    path = [(1, 1)]  # 初始化路径，起始位置

    # 继续基于 max_path 继续向下探测，直到达到矿井边界
    while path and path[-1][0] < n and path[-1][1] < n and m > 0:
        # 获取路径的最后一个位置继续探测
        x, y = path[-1]  # 使用路径最后的值

        # 检查剩余步数是否足够走下去
        if x + y < n and m > 0:
            res, path = probe_go(x, y, res, m, n, mine_field, path)
        else:
            break  # 超过步数或边界，终止探测

    # 调整路径为0-indexed格式
    adjusted_path = [(i - 1, j - 1) for i, j in path]

    print("蒙图算法的最大矿产值：", res)
    print("蒙图算法选择的路径：", adjusted_path)

    return adjusted_path

# 残缺地图
def generate_lose_map(mine_field):
    """
        随机生成残缺地图
    """
    size = len(mine_field[0]) - 1
    lose_num = random.randint(1, size * size)
    for i in range(lose_num):
        lose_x = random.randint(1, size)
        lose_y = random.randint(1, size)
        mine_field[lose_x][lose_y] = 0

    return mine_field



def lose_map(mine_field):
    """
        残缺地图情况下的路径选择
    """
    # 创建残缺地图
    lose_map = generate_lose_map(mine_field)
    print("残缺地图")
    print(lose_map)

    dp = find_max_mining_path(lose_map)
    # 获取最优路径
    dp_path = print_mining_path(dp)
    print(f"最优路径: {dp_path}")

    return dp_path
