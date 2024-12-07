import sys
import numpy as np
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton
from PyQt5.QtGui import QPainter, QColor, QPen
from PyQt5.QtCore import Qt, QTimer


class MineFieldWindow(QMainWindow):
    def __init__(self, mine_field, dp_path=None, greedy_path=None):
        super().__init__()
        self.mine_field = mine_field
        self.dp_path = dp_path
        self.greedy_path = greedy_path
        self.current_dp_index = 0
        self.current_greedy_index = 0
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Mine Field Visualization")
        self.setGeometry(100, 100, 1000, 800)

        # Initialize buttons, but don't set their geometry yet
        self.dp_button = QPushButton('DP Path', self)
        self.dp_button.clicked.connect(self.show_dp_path)

        self.greedy_button = QPushButton('Greedy Path', self)
        self.greedy_button.clicked.connect(self.show_greedy_path)

        # Timers for animation
        self.dp_timer = QTimer()
        self.dp_timer.timeout.connect(self.update_dp_path)

        self.greedy_timer = QTimer()
        self.greedy_timer.timeout.connect(self.update_greedy_path)

        self.show()

    def resizeEvent(self, event):
        self.updateButtonPositions()
        super().resizeEvent(event)

    def updateButtonPositions(self):
        # Calculate the legend position
        rows, cols = self.mine_field.shape
        cell_size = min(self.width() // cols, self.height() // rows)
        legend_x = cols * cell_size + 10  # Reduced spacing to shrink right-side whitespace
        legend_y = 20 + 4 * 30  # 4 legend items, each 30 pixels apart

        # Set button positions below the legend
        self.dp_button.setGeometry(legend_x, legend_y + 40, 120, 40)
        self.greedy_button.setGeometry(legend_x, legend_y + 90, 120, 40)

    def paintEvent(self, event):
        qp = QPainter()
        qp.begin(self)
        self.drawMineField(qp)
        self.drawPaths(qp)
        qp.end()

    def drawMineField(self, qp):
        rows, cols = self.mine_field.shape
        cell_size = min(self.width() // cols, self.height() // rows)

        for i in range(rows):
            for j in range(cols):
                value = self.mine_field[i, j]
                if value == 0:
                    qp.setBrush(QColor(255, 255, 255))  # White for no mines
                else:
                    color_intensity = min(255, int(value / 1000 * 255))
                    qp.setBrush(QColor(color_intensity, 255 - color_intensity, 0))  # Red to Green gradient

                qp.drawRect(j * cell_size, i * cell_size, cell_size, cell_size)

                if value > 0:
                    qp.setPen(QPen(Qt.white))
                    qp.drawText(j * cell_size + cell_size // 4, i * cell_size + cell_size // 2, f'{value:.1f}')

        qp.setPen(QPen(Qt.black, 1, Qt.SolidLine))
        for i in range(rows + 1):
            qp.drawLine(0, i * cell_size, cols * cell_size, i * cell_size)
        for j in range(cols + 1):
            qp.drawLine(j * cell_size, 0, j * cell_size, rows * cell_size)

        # Draw legend
        legend_x = cols * cell_size + 10  # Reduced spacing
        legend_y = 20

        # Legend for cell colors
        qp.setPen(QPen(Qt.black))
        qp.setBrush(QColor(255, 0, 0))  # Red
        qp.drawRect(legend_x, legend_y, 20, 20)
        qp.drawText(legend_x + 30, legend_y + 15, "High Value")

        legend_y += 30
        qp.setBrush(QColor(0, 255, 0))  # Green
        qp.drawRect(legend_x, legend_y, 20, 20)
        qp.drawText(legend_x + 30, legend_y + 15, "Low Value")

        # Legend for paths
        legend_y += 30
        qp.setPen(QPen(QColor(255, 165, 0), 3, Qt.SolidLine))  # 亮橙色
        qp.drawLine(legend_x, legend_y + 10, legend_x + 20, legend_y + 10)
        qp.drawText(legend_x + 30, legend_y + 15, "DP Path")

        legend_y += 30
        qp.setPen(QPen(QColor(238, 130, 238), 3, Qt.DashLine))  # 紫罗兰色
        qp.drawLine(legend_x, legend_y + 10, legend_x + 20, legend_y + 10)
        qp.drawText(legend_x + 30, legend_y + 15, "Greedy Path")

    def drawPaths(self, qp):
        cell_size = min(self.width() // self.mine_field.shape[1], self.height() // self.mine_field.shape[0])

        # Draw part of the DP path
        if self.dp_path:
            qp.setPen(QPen(QColor(255, 165, 0), 3, Qt.SolidLine))  # 亮橙色
            for k in range(self.current_dp_index - 1):
                start = self.dp_path[k]
                end = self.dp_path[k + 1]
                qp.drawLine(start[1] * cell_size + cell_size // 2, start[0] * cell_size + cell_size // 2,
                            end[1] * cell_size + cell_size // 2, end[0] * cell_size + cell_size // 2)

        # Draw part of the Greedy path
        if self.greedy_path:
            qp.setPen(QPen(QColor(238, 130, 238), 3, Qt.DashLine))  # 紫罗兰色
            for k in range(self.current_greedy_index - 1):
                start = self.greedy_path[k]
                end = self.greedy_path[k + 1]
                qp.drawLine(start[1] * cell_size + cell_size // 2, start[0] * cell_size + cell_size // 2,
                            end[1] * cell_size + cell_size // 2, end[0] * cell_size + cell_size // 2)

    def show_dp_path(self):
        self.current_dp_index = 0
        self.dp_timer.start(100)  # Start timer with 100 ms interval

    def update_dp_path(self):
        if self.current_dp_index < len(self.dp_path):
            self.current_dp_index += 1
            self.update()
        else:
            self.dp_timer.stop()

    def show_greedy_path(self):
        self.current_greedy_index = 0
        self.greedy_timer.start(100)  # Start timer with 100 ms interval

    def update_greedy_path(self):
        if self.current_greedy_index < len(self.greedy_path):
            self.current_greedy_index += 1
            self.update()
        else:
            self.greedy_timer.stop()

def visualize_mine_field(mine_field, dp_path=None, greedy_path=None):
    app = QApplication(sys.argv)
    ex = MineFieldWindow(mine_field, dp_path, greedy_path)
    sys.exit(app.exec_())

# Example usage with dummy data
if __name__ == "__main__":
    mine_field = np.random.randint(0, 1000, (10, 10))
    dp_path = [(i, i) for i in range(10)]  # Example DP path
    greedy_path = [(i, 9-i) for i in range(10)]  # Example Greedy path
    visualize_mine_field(mine_field, dp_path, greedy_path)