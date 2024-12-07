def greedy_probe(x, y, curr, n, map_data, ans_probe_1, path, best_path):
    if x + y == n + 1:  # 到达金字塔底部
        if curr > ans_probe_1[0]:
            ans_probe_1[0] = curr
            best_path[:] = path[:]  # 记录当前最优路径
        return

    # 选择向下或向右的路径
    if map_data[x + 1][y] > map_data[x][y + 1]:
        # 先走下边，记录当前位置
        path.append((x + 1, y))
        greedy_probe(x + 1, y, curr + map_data[x + 1][y], n, map_data, ans_probe_1, path, best_path)
        path.pop()  # 回溯，移除最后一步
    else:
        # 先走右边，记录当前位置
        path.append((x, y + 1))
        greedy_probe(x, y + 1, curr + map_data[x][y + 1], n, map_data, ans_probe_1, path, best_path)
        path.pop()  # 回溯，移除最后一步

def probe_1(n, map_data):
    ans_probe_1 = [0]  # 用列表来模拟引用传递
    best_path = []  # 用于记录最佳路径
    path = [(1, 1)]  # 初始路径从 (0, 0) 开始

    # 贪心搜索
    greedy_probe(1, 1, map_data[1][1], n, map_data, ans_probe_1, path, best_path)

    # 输出路径时需要减去1
    adjusted_path = [(i - 1, j - 1) for i, j in best_path]  # 适当调整路径上的坐标

    print(f"最大路径和: {ans_probe_1[0]}")
    print("贪心算法选择的路径:", adjusted_path)


    return adjusted_path
