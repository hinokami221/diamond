import unittest
import numpy as np
from limit_dynamic import probe_m

class TestLimitDynamic(unittest.TestCase):
    def setUp(self):
        # 从文件读取多个测试数据
        self.dataList, self.layerList, self.stepList, self.predict_maxList, self.predict_pathList = self.load_test_data('test_limit_dynamic.txt')

    def load_test_data(self, file_path):
        dataList = []  # 存储数据块
        layerList = []  # 存储层数
        stepList = []  # 存储探测的步数
        predict_maxList = []  # 存储预测最大值
        predict_pathList = []  # 存储预测路径

        with open(file_path, 'r') as file:
            current_data = []
            current_max = None
            current_step = None
            current_layer = None
            current_path = []
            reading_data = False
            reading_path = False
            reading_layer = False
            reading_step = False
            reading_max = False

            for line in file:
                line = line.strip()  # 去除行首尾空白字符

                if line == "data":
                    if current_data:
                        dataList.append(np.array(current_data))
                    reading_data = True
                    reading_path = False
                    current_data = []
                elif line == "layer":
                    if current_layer is not None:
                        layerList.append(current_layer)
                    reading_data = False
                    reading_path = False
                    reading_layer = True
                    current_layer = None
                elif line == "step":
                    if current_step is not None:
                        stepList.append(current_step)
                    reading_data = False
                    reading_path = False
                    reading_step = True
                    current_step = None
                elif line == "max":
                    if current_max is not None:
                        predict_maxList.append(current_max)
                    reading_data = False
                    reading_path = False
                    reading_max = True
                    current_max = None
                elif line == "path":
                    if current_path:
                        predict_pathList.append(current_path)
                    reading_data = False
                    reading_path = True
                    current_path = []
                elif reading_data:
                    current_data.append(list(map(int, line.split())))
                elif reading_path:
                    numbers = line.strip().split()
                    current_path.append((int(numbers[0]), int(numbers[1])))
                elif reading_max:
                    current_max = int(line)
                    reading_max = False
                elif reading_step:
                    current_step = int(line)
                    reading_step = False
                elif reading_layer:
                    current_layer = int(line)
                    reading_layer = False

            # 处理最后的数据块
            if current_data:
                dataList.append(np.array(current_data))
            if current_max is not None:
                predict_maxList.append(current_max)
            if current_step is not None:
                stepList.append(current_step)
            if current_layer is not None:
                layerList.append(current_layer)
            if current_path:
                predict_pathList.append(current_path)

        return dataList, layerList, stepList, predict_maxList, predict_pathList

    def test_probe_m(self):
        size = len(self.dataList)
        for i in range(size):
            path = probe_m(self.layerList[i], self.dataList[i], self.stepList[i])
            self.assertEqual(path, self.predict_pathList[i], f"第 {i} 个测试中路径出错，预期: {self.predict_pathList[i]}, 实际: {path}")
