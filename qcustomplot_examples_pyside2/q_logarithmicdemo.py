'''
****************************************************************************
**                                                                        **
**  QCustomPlot Pyside2 bindings are Python bindings for QCustomPlot/Qt   **
**                                                                        **
**                                                                        **
**  This program is free software: you can redistribute it and/or modify  **
**  it under the terms of the GNU General Public License as published by  **
**  the Free Software Foundation, either version 3 of the License, or     **
**  (at your option) any later version.                                   **
**                                                                        **
**  This program is distributed in the hope that it will be useful,       **
**  but WITHOUT ANY WARRANTY; without even the implied warranty of        **
**  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         **
**  GNU General Public License for more details.                          **
**                                                                        **
**  You should have received a copy of the GNU General Public License     **
**  along with this program.  If not, see http://www.gnu.org/licenses/.   **
**                                                                        **
****************************************************************************
**  Website/Contact: https://github.com/SBGit-2019/Pyside-QCP             **
****************************************************************************
'''

import shiboken2 as Shiboken
from PySide2 import QtGui
import sys
import math
from random import uniform,randint
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout,QWidget,QMainWindow
from PySide2.QtGui import QLinearGradient, QRadialGradient, QColor, QBrush, QPen, QFont, QPixmap, QPainterPath, QGuiApplication
from PySide2.QtCore import Qt, QMargins,QPointF,QObject,QCoreApplication,QFile,QTimer,QLocale,QDateTime,QDate,QSize,QTime
from PySide2.QtUiTools import QUiLoader
from qcustomplot_pyside2 import *


def demo(app, demotime=0):
    customPlot = QCustomPlot()
    screen = QGuiApplication.primaryScreen().geometry()
    customPlot.resize(screen.height(), screen.height()*0.75)
    customPlot.setWindowTitle('Logarithmic Demo')

    customPlot.setNoAntialiasingOnDrag(True) # more performance/responsiveness during dragging
    customPlot.addGraph()
    pen = QPen()
    pen.setColor(QColor(255,170,100))
    pen.setWidth(2)
    pen.setStyle(Qt.DotLine)
    customPlot.graph(0).setPen(pen)
    customPlot.graph(0).setName("x")

    customPlot.addGraph()
    customPlot.graph(1).setPen(QPen(Qt.red))
    customPlot.graph(1).setBrush(QBrush(QColor(255, 0, 0, 20)))
    customPlot.graph(1).setName("-sin(x)exp(x)")

    customPlot.addGraph()
    customPlot.graph(2).setPen(QPen(Qt.blue))
    customPlot.graph(2).setBrush(QBrush(QColor(0, 0, 255, 20)))
    customPlot.graph(2).setName(" sin(x)exp(x)")

    customPlot.addGraph()
    pen.setColor(QColor(0,0,0))
    pen.setWidth(1)
    pen.setStyle(Qt.DashLine)
    customPlot.graph(3).setPen(pen)
    customPlot.graph(3).setBrush(QBrush(QColor(0,0,0,15)))
    customPlot.graph(3).setLineStyle(QCPGraph.lsStepCenter)
    customPlot.graph(3).setName("x!")

    dataCount = 200
    dataFactorialCount = 21
    # Use tuples instead of lists
    dataLinear = [(0.0,0.0)] * dataCount
    # Use lists
    dataMinusSinExpX =  [0.0] * dataCount
    dataMinusSinExpY =  [0.0] * dataCount
    dataPlusSinExpX =  [0.0] * dataCount
    dataPlusSinExpY =  [0.0] * dataCount
    dataFactorialX =  [0.0] * dataFactorialCount
    dataFactorialY =  [0.0] * dataFactorialCount

    for i in range(0, dataCount):
      dataLinear[i] = (float(i)/10.0,float(i)/10.0)
      dataMinusSinExpX[i]= float(i)/10.0
      dataMinusSinExpY[i]= -math.sin(dataMinusSinExpX[i])*math.exp(dataMinusSinExpX[i])
      dataPlusSinExpX[i]= float(i)/10.0
      dataPlusSinExpY[i]= math.sin(dataPlusSinExpX[i])*math.exp(dataPlusSinExpX[i])

    for i in range(0, dataFactorialCount):
      dataFactorialX[i]= float(i)
      dataFactorialY[i]= 1.0
      for k in range(1, i+1): # factorial
        dataFactorialY[i]*= k

    # Split tuples to two lists
    list1, list2 = zip(*dataLinear)
    customPlot.graph(0).setData(list1, list2)
    customPlot.graph(1).setData(dataMinusSinExpX,dataMinusSinExpY)
    customPlot.graph(2).setData(dataPlusSinExpX,dataPlusSinExpY)
    customPlot.graph(3).setData(dataFactorialX,dataFactorialY)

    xAxis = customPlot.xAxis
    yAxis = customPlot.yAxis
    gridX = xAxis.grid()
    gridY = yAxis.grid()
    gridX.setSubGridVisible(True)
    gridY.setSubGridVisible(True)
    customPlot.yAxis.setScaleType(QCPAxis.stLogarithmic)
    customPlot.yAxis2.setScaleType(QCPAxis.stLogarithmic)

    logTicker = QCPAxisTickerLog()
    logTicker2 = QCPAxisTickerLog()
    customPlot.yAxis.setTicker(logTicker)
    customPlot.yAxis2.setTicker(logTicker2)
    customPlot.yAxis.setNumberFormat("eb") # e = exponential, b = beautiful decimal powers
    customPlot.yAxis.setNumberPrecision(0) # makes sure "1*10^4" is displayed only as "10^4"
    customPlot.xAxis.setRange(0, 19.9)
    customPlot.yAxis.setRange(1e-2, 1e10)

    # make range draggable and zoomable:
    customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom)
    customPlot.axisRect().setupFullAxesBox()

    # make top right axes clones of bottom left axes:
    customPlot.legend.setVisible(True)
    customPlot.legend.setBrush(QBrush(QColor(255,255,255,150)))
    customPlot.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignLeft|Qt.AlignTop)
    # connect signals so top and right axes move in sync with bottom and left axes:
    customPlot.xAxis.rangeChanged.connect(customPlot.xAxis2.setRange)
    customPlot.yAxis.rangeChanged.connect(customPlot.yAxis2.setRange)

    closeTimer = QTimer()
    closeTimer.timeout.connect(customPlot.close)
    if demotime > 0:
        closeTimer.start(demotime)
    customPlot.show()


    # Create and show the form
    # Run the main Qt loop
    res = app.exec_()
    customPlot = None
    return res


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    res = demo(app)
    sys.exit(res)

