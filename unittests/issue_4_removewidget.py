import time

from PySide2.QtCore import Qt
from PySide2.QtGui import QPen, QBrush
from PySide2.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel
from qcustomplot_pyside2 import QCustomPlot, QCP, QCPAxisTickerDateTime, QCPScatterStyle,QCPGraph


class CustomPlot(QCustomPlot):
    def __init__(self):
        super(CustomPlot, self).__init__()
        tm = time.time()
        data = [int(tm + i * 100) for i in range(100)], [i for i in range(100)]
        self.resize(800, 600)
        self.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectAxes)
        self.addGraph()
        self.graph(0).setData(data[0], data[1])
        self.graph(0).setLineStyle(QCPGraph.lsNone)
        self.graph(0).setScatterStyle(
            QCPScatterStyle(QCPScatterStyle.ssCircle, QPen(Qt.red, 1), QBrush(Qt.yellow), 6))
        #############################################
        # self must be used, and will cause a crash when removing the control
        self.dateTimeTicker = QCPAxisTickerDateTime()
        self.dateTimeTicker.setDateTimeFormat("dd hh:mm:ss")
        self.xAxis.setTicker(self.dateTimeTicker)
        #############################################
        self.legend.setVisible(True)
        self.xAxis.setLabel("Time")
        self.yAxis.setLabel("Value")
        self.rescaleAxes()


class Window(QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.resize(800, 600)
        self.setLayout(QVBoxLayout())
        self.layout().setAlignment(Qt.AlignTop)
        self.button = QPushButton("add", self)
        self.button2 = QPushButton("remove", self)
        hBoxLayout = QHBoxLayout()
        hBoxLayout.addWidget(self.button)
        hBoxLayout.addWidget(self.button2)
        self.vBoxLayout = QVBoxLayout()
        self.layout().addLayout(hBoxLayout)
        self.layout().addLayout(self.vBoxLayout)

        self.button.clicked.connect(self.add)
        self.button2.clicked.connect(self.remove)

    def add(self):
        self.vBoxLayout.addWidget(CustomPlot())
        # With normal Qt controls it doesn't crash
        # self.vBoxLayout.addWidget(QLabel("label"))

    def remove(self):
        if self.vBoxLayout.count() > 0:
            widget = self.vBoxLayout.itemAt(0).widget()
            self.vBoxLayout.removeWidget(widget)
            widget.deleteLater()



if __name__ == '__main__':
    app = QApplication()
    window = Window()
    window.show()
    app.exec_()
