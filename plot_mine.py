import matplotlib.pyplot as plt
import numpy as np


def rotate_coordinates_90(x, y):
    """
    将给定的坐标 (x, y) 逆时针旋转 90 度。

    参数：
    x, y -- 原始坐标

    返回：
    x', y' -- 旋转后的坐标
    """
    x_rot = -y  # 逆时针旋转 90 度
    y_rot = x
    return x_rot, y_rot


def rotate_coordinates_45(x, y):
    """
    将给定的坐标 (x, y) 逆时针旋转 45 度。

    参数：
    x, y -- 原始坐标

    返回：
    x'', y'' -- 旋转后的坐标
    """
    cos_45 = np.cos(np.radians(45))
    sin_45 = np.sin(np.radians(45))

    x_rot = cos_45 * x - sin_45 * y
    y_rot = sin_45 * x + cos_45 * y

    return x_rot, y_rot


def plot_mine_field(mine_field):
    """
    绘制矿产分布图，以点表示矿产的分布，先逆时针旋转 90 度，再逆时针旋转 45 度。

    参数:
    mine_field -- 矿产分布图（二维数组）
    """
    layers = mine_field.shape[0]

    # 存储旋转后的坐标和大小
    rotated_coords = []
    sizes = []

    for i in range(layers):
        for j in range(i + 1):  # 第i层有i+1个矿产位置
            # 先逆时针旋转 90 度
            x_rot_90, y_rot_90 = rotate_coordinates_90(i, j)
            # 再逆时针旋转 45 度
            x_rot_45, y_rot_45 = rotate_coordinates_45(x_rot_90, y_rot_90)

            rotated_coords.append((x_rot_45, y_rot_45))
            sizes.append(mine_field[i, j] * 5)  # 点的大小与矿产值相关

    # 计算坐标范围
    rotated_coords = np.array(rotated_coords)
    x_min, x_max = rotated_coords[:, 0].min(), rotated_coords[:, 0].max()
    y_min, y_max = rotated_coords[:, 1].min(), rotated_coords[:, 1].max()

    # 绘制
    plt.figure(figsize=(8, 8))
    for (x_rot, y_rot), size in zip(rotated_coords, sizes):
        plt.scatter(x_rot, y_rot, s=size, c='orange', alpha=0.6)  # 点的大小与矿产值相关

    plt.title("Mine Field (Rotated 90 + 45 degrees)")
    plt.xlabel("X (Rotated)")
    plt.ylabel("Y (Rotated)")

    # 设置坐标范围以适应旋转后的图形
    plt.xlim(x_min - 1, x_max + 1)
    plt.ylim(y_min - 1, y_max + 1)
    plt.gca().set_aspect('equal', adjustable='box')  # 保持纵横比一致
    plt.show()


def plot_optimal_path(mine_field, path):
    """
    绘制最优路径，并将图表先逆时针旋转 90 度，再逆时针旋转 45 度。

    参数:
    mine_field -- 矿产分布图（二维数组）
    path -- 最优路径（由(i, j)元组组成的列表）
    """
    layers = mine_field.shape[0]

    # 存储旋转后的坐标和大小
    rotated_coords = []
    path_rotated = []

    for i in range(layers):
        for j in range(i + 1):  # 第i层有i+1个矿产位置
            # 先逆时针旋转 90 度
            x_rot_90, y_rot_90 = rotate_coordinates_90(i, j)
            # 再逆时针旋转 45 度
            x_rot_45, y_rot_45 = rotate_coordinates_45(x_rot_90, y_rot_90)

            rotated_coords.append((x_rot_45, y_rot_45))

    # 获取路径的旋转坐标
    for (i, j) in path:
        x_rot_90, y_rot_90 = rotate_coordinates_90(i, j)
        x_rot_45, y_rot_45 = rotate_coordinates_45(x_rot_90, y_rot_90)
        path_rotated.append((x_rot_45, y_rot_45))

    # 计算坐标范围
    rotated_coords = np.array(rotated_coords)
    x_min, x_max = rotated_coords[:, 0].min(), rotated_coords[:, 0].max()
    y_min, y_max = rotated_coords[:, 1].min(), rotated_coords[:, 1].max()

    # 绘制
    plt.figure(figsize=(8, 8))
    for (x_rot, y_rot) in rotated_coords:
        plt.scatter(x_rot, y_rot, s=50, c='orange', alpha=0.6)  # 点的大小与矿产值相关

    # 绘制路径
    path_x = [x for x, _ in path_rotated]
    path_y = [y for _, y in path_rotated]
    plt.scatter(path_x, path_y, c='blue', s=80, edgecolor='black', label='Optimal Path')  # 最优路径的点

    plt.title("Optimal Mining Path ")
    plt.xlabel("X (Rotated)")
    plt.ylabel("Y (Rotated)")

    # 设置坐标范围以适应旋转后的图形
    plt.xlim(x_min - 1, x_max + 1)
    plt.ylim(y_min - 1, y_max + 1)
    plt.gca().set_aspect('equal', adjustable='box')  # 保持纵横比一致
    plt.legend()
    plt.show()
