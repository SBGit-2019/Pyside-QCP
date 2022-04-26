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
    # prepare data:
    x1 = [0.0] * 20
    y1 = [0.0] * 20
    for i in range(0, len(x1)):
      x1[i] = float(i)/19.0*10.0
      y1[i] = math.cos(x1[i]*0.8+math.sin(x1[i]*0.16+1.0))*math.sin(x1[i]*0.54)+1.4


    x2 = [0.0] * 100
    y2 = [0.0] * 100
    for i in range(0, len(x2)):
      x2[i] = float(i)/99.0*10.0
      y2[i] = math.cos(x2[i]*0.85+math.sin(x2[i]*0.165+1.1))*math.sin(x2[i]*0.50)+1.7

    x3 = [0.0] * 20
    y3 = [0.0] * 20
    for i in range(0, len(x3)):
      x3[i] = float(i)/19.0*10.0
      y3[i] = 0.05+3*(0.5+math.cos(x3[i]*x3[i]*0.2+2)*0.5)/(x3[i]+0.7)+uniform(0,1)*0.01

    x4 = [0.0] * 20
    y4 = [0.0] * 20
    for i in range(0, len(x4)):
      x4[i] = x3[i];
      y4[i] = (0.5-y3[i])+((x4[i]-2.0)*(x4[i]-2.0)*0.02)

    customPlot = QCustomPlot()
    screen = QGuiApplication.primaryScreen().geometry()
    customPlot.resize(screen.height(), screen.height()*0.75)
    customPlot.setWindowTitle('QCustomPlot Pyside2 Demo II')

    # create and configure plottables:
    graph1 = customPlot.addGraph()
    graph1.setData(x1,y1)
    graph1.setPen(QPen(QColor(120, 120, 120), 2))
    graph1.setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, QPen(Qt.black, 1.5), QBrush(Qt.white), 9))

    graph2 = customPlot.addGraph()
    graph2.setData(x2,y2)
    graph2.setPen(Qt.NoPen)
    graph2.setBrush(QColor(200, 200, 200, 20))
    graph2.setChannelFillGraph(graph1)

    bars1 = QCPBars(customPlot.xAxis, customPlot.yAxis)
    bars1.setWidth(9.0/20.0)
    bars1.setData(x3, y3)
    bars1.setPen(Qt.NoPen);
    bars1.setBrush(QColor(10, 140, 70, 160))

    bars2 = QCPBars(customPlot.xAxis, customPlot.yAxis)
    bars2.setWidth(9.0/20.0)
    bars2.setData(x4, y4)
    bars2.setPen(Qt.NoPen)
    bars2.setBrush(QColor(10, 100, 50, 70))
    bars2.moveAbove(bars1)

    # move bars above graphs and grid below bars:
    layer = customPlot.layer("main")
    customPlot.addLayer("abovemain", layer, QCustomPlot.limAbove)
    customPlot.addLayer("belowmain", layer, QCustomPlot.limBelow)
    graph1.setLayer("abovemain")

    xaxis = customPlot.xAxis
    yaxis = customPlot.yAxis
    grid = xaxis.grid()
    grid.setLayer("belowmain")
    yaxis.grid().setLayer("belowmain")

    # set some pens, brushes and backgrounds:
    customPlot.xAxis.setBasePen(QPen(Qt.white, 1))
    customPlot.yAxis.setBasePen(QPen(Qt.white, 1))
    customPlot.xAxis.setTickPen(QPen(Qt.white, 1))
    customPlot.yAxis.setTickPen(QPen(Qt.white, 1))
    customPlot.xAxis.setSubTickPen(QPen(Qt.white, 1))
    customPlot.yAxis.setSubTickPen(QPen(Qt.white, 1))
    customPlot.xAxis.setTickLabelColor(Qt.white)
    customPlot.yAxis.setTickLabelColor(Qt.white)

    xaxis.grid().setPen(QPen(QColor(140, 140, 140), 1, Qt.DotLine))
    yaxis.grid().setPen(QPen(QColor(140, 140, 140), 1, Qt.DotLine))
    xaxis.grid().setSubGridPen(QPen(QColor(80, 80, 80), 1, Qt.DotLine))
    yaxis.grid().setSubGridPen(QPen(QColor(80, 80, 80), 1, Qt.DotLine))
    xaxis.grid().setSubGridVisible(True)
    yaxis.grid().setSubGridVisible(True)
    xaxis.grid().setZeroLinePen(Qt.NoPen)
    yaxis.grid().setZeroLinePen(Qt.NoPen)

    lineEnd = QCPLineEnding.esSpikeArrow
    lineEnd2 = QCPLineEnding(QCPLineEnding.esSpikeArrow)
    xaxis.setUpperEnding(lineEnd2)
    yaxis.setUpperEnding(lineEnd2)

    plotGradient = QLinearGradient()
    plotGradient.setStart(0, 0)
    plotGradient.setFinalStop(0, 350)
    plotGradient.setColorAt(0, QColor(80, 80, 80))
    plotGradient.setColorAt(1, QColor(50, 50, 50))
    customPlot.setBackground(plotGradient)

    axisRectGradient = QLinearGradient()
    axisRectGradient.setStart(0, 0)
    axisRectGradient.setFinalStop(0, 350)
    axisRectGradient.setColorAt(0, QColor(80, 80, 80))
    axisRectGradient.setColorAt(1, QColor(30, 30, 30))
    customPlot.axisRect().setBackground(axisRectGradient)



    font = QtGui.QFont()
    font.setPointSize(12)
    color = QColor(Qt.white)

    textGradient = QLinearGradient()
    textGradient.setStart(0, 0)
    textGradient.setFinalStop(0, 100)
    textGradient.setColorAt(0, QColor(255, 0, 0, 50))
    textGradient.setColorAt(1, QColor(0, 0, 255, 50))

    groupTracerText = QCPItemText(customPlot)
    groupTracerText.setPositionAlignment(Qt.AlignRight|Qt.AlignTop)
    groupTracerText.setPen(QPen(QColor(255, 255, 255, 80), 1))
    groupTracerText.setColor(Qt.white)
    groupTracerText.setBrush(textGradient)
    pos =  groupTracerText.position()
    pos.setType(QCPItemPosition.ptAxisRectRatio)
    pos.setCoords(0.85, 0.3)
    groupTracerText.setText("\nThis is an example \nplot label text!\n")
    groupTracerText.setTextAlignment(Qt.AlignLeft)
    groupTracerText.setFont(font)
    groupTracerText.setPadding(QMargins(8, 0, 0, 0))

    customPlot.rescaleAxes()
    customPlot.yAxis.setRange(0, 2)

    closeTimer = QTimer()
    closeTimer.timeout.connect(customPlot.close)
    if demotime > 0:
        closeTimer.start(demotime)
    customPlot.show()
    res = app.exec_()
    customPlot = None
    return res


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    res = demo(app)
    sys.exit(res)




