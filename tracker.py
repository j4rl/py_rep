import math
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton
from PyQt5.QtGui import QPainter, QPen, QPainterPath
from PyQt5.QtCore import Qt
import sys
import numpy as np

class Axes(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
    
    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 1, Qt.DashLine)
        painter.setPen(pen)
        
        rect = self.rect()
        width = rect.width()
        height = rect.height()
        
        # Draw x-axis
        painter.drawLine(0, int(height / 2), width, int(height / 2))
        
        # Draw y-axis
        painter.drawLine(int(width / 2), 0, int(width / 2), height)

class PlotWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Math Expression Plotter")
        self.setGeometry(100, 100, 800, 600)
        
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        
        self.layout = QVBoxLayout(self.central_widget)
        
        self.expression_input = QLineEdit(self)
        self.expression_input.setPlaceholderText("Enter a math expression (e.g., sin(x), cos(x), x**2)")
        self.layout.addWidget(self.expression_input)
        
        self.plot_button = QPushButton("Plot", self)
        self.plot_button.clicked.connect(self.plot_expression)
        self.layout.addWidget(self.plot_button)
        
        self.axes = Axes(self)
        self.layout.addWidget(self.axes)
        
        self.plot_area = PlotArea(self)
        self.layout.addWidget(self.plot_area)
    
    def plot_expression(self):
        expression = self.expression_input.text()
        self.plot_area.set_expression(expression)
        self.plot_area.repaint()

class PlotArea(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.expression = ""
    
    def set_expression(self, expression):
        self.expression = expression
    
    def paintEvent(self, event):
        if not self.expression:
            return
        
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        pen = QPen(Qt.black, 2)
        painter.setPen(pen)
        
        rect = self.rect()
        width = rect.width()
        height = rect.height()
        
        try:
            x = np.linspace(-10, 10, width)
            y = eval(self.expression, {"x": x, "np": np, "math": math})
        except Exception as e:
            print(f"Error evaluating expression: {e}")
            return
        
        y = np.clip(y, -10, 10)
        y = height / 2 - (y * height / 20)
        
        path = QPainterPath()
        path.moveTo(0, y[0])
        for i in range(1, len(x)):
            path.lineTo(i, y[i])
        
        painter.drawPath(path)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = PlotWindow()
    window.show()
    sys.exit(app.exec_())


