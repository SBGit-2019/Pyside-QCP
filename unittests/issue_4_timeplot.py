import time
from PySide2.QtWidgets import QApplication
from qcustomplot_pyside2 import QCustomPlot, QCP, QCPAxisTickerDateTime, QCPScatterStyle

#from PyQt5.QtWidgets import QApplication
#from QCustomPlot2 import QCustomPlot, QCP, QCPAxisTickerDateTime, QCPScatterStyle

app = QApplication([])
customPlot = QCustomPlot()
customPlot.resize(800, 600)
customPlot.setInteractions(QCP.iRangeZoom)
customPlot.addGraph()
tm = time.time()
data = [tm + i *1000 for i in range(100)], [0 for i in range(100)]
customPlot.graph(0).setData(*data)
customPlot.graph(0).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, 5))
dateTimeTicker = QCPAxisTickerDateTime()
dateTimeTicker.setDateTimeFormat("dd hh:mm:ss")
customPlot.xAxis.setTicker(dateTimeTicker)
customPlot.legend.setVisible(True)
customPlot.xAxis.setLabel("Time")
customPlot.yAxis.setLabel("Value")
customPlot.rescaleAxes()
customPlot.show()
app.exec_()

