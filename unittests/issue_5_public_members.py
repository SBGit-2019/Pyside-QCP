from PySide2.QtCore import Qt
from PySide2.QtGui import QPen
from PySide2.QtWidgets import QApplication
from qcustomplot_pyside2 import QCustomPlot, QCP, QCPScatterStyle, QCPItemStraightLine

# from PyQt5.QtCore import Qt
# from PyQt5.QtGui import QPen
# from PyQt5.QtWidgets import QApplication
# from QCustomPlot2 import QCustomPlot, QCP, QCPScatterStyle, QCPItemStraightLine

app = QApplication([])
customPlot = QCustomPlot()
customPlot.resize(800, 600)
customPlot.setInteractions(QCP.iRangeDrag)
customPlot.addGraph()
data = [i for i in range(100)], [i for i in range(100)]
customPlot.graph(0).setData(*data)
customPlot.graph(0).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, 5))
customPlot.legend.setVisible(True)
customPlot.xAxis.setLabel("Time")
customPlot.yAxis.setLabel("Value")
infLine = QCPItemStraightLine(customPlot)
infLine.setPen(QPen(Qt.red))
##############################################################################################
# Unable to add infinite lines to plot
# AttributeError: 'QCustomPlot.QCPItemStraightLine' object has no attribute 'point1'
infLine.point1.setCoords(50, 0)
infLine.get_point2().setCoords(50, 1)
##############################################################################################
customPlot.rescaleAxes()
customPlot.show()
app.exec_()
