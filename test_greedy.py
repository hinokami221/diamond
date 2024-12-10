import unittest
import numpy as np
from greedy import probe_1


class TestDynamic(unittest.TestCase):
    def setUp(self):
        # 从文件读取多个测试数据
        self.dataList, self.layerList, self.predict_maxList, self.predict_pathList = self.load_test_data('test_greedy.txt')

    def load_test_data(self, file_path):
        # 读取文件并生成多个二维数组
        dataList = []  # 存储数据块
        layerList = []  # 存储层数
        predict_maxList = []  # 存储预测最大值
        predict_pathList = []  # 存储预测路径

        with open(file_path, 'r') as file:
            current_data = []  # 存储当前数据块
            current_max = None  # 存储当前最大值
            current_layer = None # 存储层数
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
                elif line == "layer":
                    if current_layer is not None:  # 如果当前层数不为空
                        layerList.append(current_layer)
                    reading_data = False  # 结束读取数据
                    reading_path = False
                    current_layer = None  # 重置当前层数
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
                elif current_layer is None:
                    # 如果当前在 layer 部分，读取层数
                    current_layer = int(line)
                elif current_max is None:
                    # 如果当前在 max 部分，读取最大值
                    current_max = int(line)
                elif reading_path:
                    # 如果当前在 path 部分，读取路径
                    numbers = line.strip().split()
                    current_path.append((int(numbers[0]), int(numbers[1])))
            if current_data:  # 如果当前数据块不为空
                dataList.append(np.array(current_data))
            if current_layer is not None:  # 如果当前最大值不为空
                layerList.append(current_layer)
            if current_max is not None:  # 如果当前最大值不为空
                layerList.append(current_max)
            if current_path:
                predict_pathList.append(current_path)  # 添加当前路径

        return dataList, layerList, predict_maxList, predict_pathList

    def test_probe_1(self):
        size = len(self.dataList)
        for i in range(size):
            path = probe_1(self.layerList[i], self.dataList[i])
            self.assertEqual(path, self.predict_pathList[i], f"第 {i} 个测试中最短路径出错")
