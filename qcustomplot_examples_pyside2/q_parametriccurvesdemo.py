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
    # generate the curve data points:
    pointCount = 500

    dataSpiral1X = [0.0] * pointCount
    dataSpiral1Y = [0.0] * pointCount
    dataSpiral2X = [0.0] * pointCount
    dataSpiral2Y = [0.0] * pointCount
    dataDeltoidX = [0.0] * pointCount
    dataDeltoidY = [0.0] * pointCount
    for i in range(0, pointCount):
      phi = float(i)/float(pointCount-1)*8.0*math.pi
      theta = float(i)/float(pointCount-1)*2.0*math.pi;
      dataSpiral1X[i] = math.sqrt(phi)*math.cos(phi)
      dataSpiral1Y[i] = math.sqrt(phi)*math.sin(phi)
      dataSpiral2X[i] = -dataSpiral1X[i]
      dataSpiral2Y[i] = -dataSpiral1Y[i]
      dataDeltoidX[i] = 2.0*math.cos(2.0*theta)+math.cos(1.0*theta)+2.0*math.sin(theta)
      dataDeltoidY[i] = 2.0*math.sin(2.0*theta)-math.sin(1.0*theta)

    customPlot = QCustomPlot()
    screen = QGuiApplication.primaryScreen().geometry()
    customPlot.resize(screen.height(), screen.height()*0.75)
    customPlot.setWindowTitle('Parametric Curves Demo')

    # pass the data to the curves; we know t (i in loop above) is ascending, so set alreadySorted=true (saves an extra internal sort):
    fermatSpiral1 = QCPCurve(customPlot.xAxis, customPlot.yAxis)
    fermatSpiral1.setData(dataSpiral1X,dataSpiral1Y)
    data = fermatSpiral1.data()
    # Just to test the data access
    fermatSpiral1.setData(data[0], data[1], data[2]);


    fermatSpiral2 = QCPCurve(customPlot.xAxis, customPlot.yAxis)
    fermatSpiral2.setData(dataSpiral2X,dataSpiral2Y)

    deltoidRadial = QCPCurve(customPlot.xAxis, customPlot.yAxis)
    deltoidRadial.setData(dataDeltoidX,dataDeltoidY)

    # color the curves:
    fermatSpiral1.setPen(QPen(Qt.blue))
    fermatSpiral1.setBrush(QBrush(QColor(0, 0, 255, 20)))
    fermatSpiral2.setPen(QPen(QColor(255, 120, 0)))
    fermatSpiral2.setBrush(QBrush(QColor(255, 120, 0, 30)))

    radialGrad = QRadialGradient(QPointF(310, 180), 200)
    radialGrad.setColorAt(0, QColor(170, 20, 240, 100))
    radialGrad.setColorAt(0.5, QColor(20, 10, 255, 40))
    radialGrad.setColorAt(1,QColor(120, 20, 240, 10))
    deltoidRadial.setPen(QPen(QColor(170, 20, 240)))
    deltoidRadial.setBrush(QBrush(radialGrad))

    # set some basic customPlot config:
    customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectPlottables)
    customPlot.axisRect().setupFullAxesBox()
    customPlot.rescaleAxes()

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



