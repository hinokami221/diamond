import unittest
import numpy as np
from all_dynamic import find_max_mining_path, print_mining_path


class TestAllDynamic(unittest.TestCase):
    def setUp(self):
        # 从文件读取多个测试数据
        self.dataList, self.predict_maxList, self.predict_pathList = self.load_test_data('test_all_dynamic.txt')

    def load_test_data(self, file_path):
        # 读取文件并生成多个二维数组
        dataList = []  # 存储数据块
        predict_maxList = []  # 存储预测最大值
        predict_pathList = []  # 存储预测路径

        with open(file_path, 'r') as file:
            current_data = []  # 存储当前数据块
            current_max = None  # 存储当前最大值
            current_path = []  # 存储当前路径
            reading_data = False  # 标记是否正在读取 data 部分
            reading_path = False  # 标记是否正在读取 path 部分

            for line in file:
                line = line.strip()  # 去除行首尾空白字符

                if line == "data":
                    if current_data:  # 如果当前数据块不为空
                        dataList.append(np.array(current_data))
                    reading_data = True  # 开始读取数据
                    reading_path = False
                    current_data = []  # 重置当前数据块
                elif line == "max":
                    if current_max is not None:  # 如果当前最大值不为空
                        predict_maxList.append(current_max)
                    reading_data = False  # 结束读取数据
                    reading_path = False
                    current_max = None  # 重置当前最大值
                elif line == "path":
                    if current_path:
                        predict_pathList.append(current_path)  # 添加当前路径
                    reading_data = False  # 结束读取数据
                    reading_path = True
                    current_path = []  # 重置当前路径
                elif reading_data:
                    # 当处于 data 部分时，将行中的数字转换为列表并添加到当前数据块
                    current_data.append(list(map(int, line.split())))
                elif current_max is None:
                    # 如果当前在 max 部分，读取最大值
                    current_max = int(line)
                elif reading_path:
                    # 如果当前在 path 部分，读取路径
                    numbers = line.strip().split()
                    current_path.append((int(numbers[0]), int(numbers[1])))
            if current_data:  # 如果当前数据块不为空
                dataList.append(np.array(current_data))
            if current_max is not None:  # 如果当前最大值不为空
                predict_maxList.append(current_max)
            if current_path:
                predict_pathList.append(current_path)  # 添加当前路径

        return dataList, predict_maxList, predict_pathList

    def test_find_max_mining_path(self):
        size = len(self.dataList)
        for i in range(size):
            dp = find_max_mining_path(self.dataList[i])
            # 计算最大矿产值
            max_value = np.max(dp)
            self.assertEqual(max_value, self.predict_maxList[i], f"第 {i} 个测试中最大值出错")

    def test_print_mining_path(self):
        size = len(self.dataList)
        for i in range(size):
            dp = find_max_mining_path(self.dataList[i])
            path = print_mining_path(dp)
            self.assertEqual(path, self.predict_pathList[i], f"第 {i} 个测试中最短路径出错")