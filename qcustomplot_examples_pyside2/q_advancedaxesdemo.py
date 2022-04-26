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
    customPlot.setWindowTitle('Advanced Axes Demo')

    # configure axis rect:
    customPlot.plotLayout().clear()
    wideAxisRect = QCPAxisRect(customPlot)
    wideAxisRect.setupFullAxesBox(True)
    wideAxisRect.axis(QCPAxis.atRight, 0).setTickLabels(True)
    wideAxisRect.addAxis(QCPAxis.atLeft).setTickLabelColor(QColor("#6050F8")) # add an extra axis on the left and color its numbers

    subLayout = QCPLayoutGrid()
    customPlot.plotLayout().addElement(0, 0, wideAxisRect) # insert axis rect in first row
    customPlot.plotLayout().addElement(1, 0, subLayout)  # sub layout in second row (grid layout will grow accordingly)
    # prepare axis rects that will be placed in the sublayout:
    subRectLeft = QCPAxisRect(customPlot, False) # false means to not setup default axes

    subRectRight = QCPAxisRect(customPlot, False)
    subLayout.addElement(0, 0, subRectLeft)
    subLayout.addElement(0, 1, subRectRight)
    subRectRight.setMaximumSize(100, 100) # make bottom right axis rect size fixed 100x100
    subRectRight.setMinimumSize(100, 100) # make bottom right axis rect size fixed 100x100

    # setup axes in sub layout axis rects:
    subRectLeft.addAxes(QCPAxis.atBottom | QCPAxis.atLeft)
    subRectRight.addAxes(QCPAxis.atBottom | QCPAxis.atRight)
    subRectLeft.axis(QCPAxis.atLeft).ticker().setTickCount(2)
    subRectRight.axis(QCPAxis.atRight).ticker().setTickCount(2)
    subRectRight.axis(QCPAxis.atBottom).ticker().setTickCount(2)
    subRectLeft.axis(QCPAxis.atBottom).grid().setVisible(True)

    # synchronize the left and right margins of the top and bottom axis rects:
    marginGroup = QCPMarginGroup(customPlot)
    subRectLeft.setMarginGroup(QCP.msLeft, marginGroup)
    subRectRight.setMarginGroup(QCP.msRight, marginGroup)
    wideAxisRect.setMarginGroup(QCP.msLeft | QCP.msRight, marginGroup)

    # move newly created axes on "axes" layer and grids on "grid" layer:
    rects = customPlot.axisRects()
    for rect in rects:
      axes = rect.axes()
      for axis in axes:
        axis.setLayer("axes")
        axis.grid().setLayer("grid")

    # prepare data:
    dataCosX = [0.0] * 21
    dataCosY = [0.0] * 21
    dataGaussX = [0.0] * 50
    dataGaussY = [0.0] * 50
    dataRandomX = [0.0] * 100
    dataRandomY = [0.0] * 100
    for i in range(0, len(dataCosX)):
      dataCosX[i] = float(i)/float(len(dataCosX)-1)*10.0-5.0
      dataCosY[i] = math.cos(dataCosX[i])

    for i in range(0, len(dataGaussX)):
      dataGaussX[i] = float(i)/float(len(dataGaussX))*10.0-5.0
      dataGaussY[i] = math.exp(-dataGaussX[i]*dataGaussX[i]*0.2)*1000

    for i in range(0, len(dataRandomX)):
      dataRandomX[i] = float(i)/float(len(dataRandomX))*10.0
      dataRandomY[i] = uniform(0.0,1.0)-0.5+dataRandomY[max(0,i-1)]

    rMax = max (dataRandomY)
    rMin = min(dataRandomY)
    rAbs = max(abs(rMax),abs(rMin))
    rInt = int(round(rAbs))

    x3 = [1,2,3,4]
    y3 = [2.0,2.5, 4.0,1.5]

    # create and configure plottables:
    mainGraphCos = customPlot.addGraph(wideAxisRect.axis(QCPAxis.atBottom), wideAxisRect.axis(QCPAxis.atLeft))
    mainGraphCos.setData(dataCosX, dataCosY)
    mainGraphCos.valueAxis().setRange(-1, 1)
    mainGraphCos.rescaleKeyAxis()
    mainGraphCos.setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, QPen(Qt.black), QBrush(Qt.white), 6))
    mainGraphCos.setPen(QPen(QColor(120, 120, 120), 2))


    mainGraphGauss = customPlot.addGraph(wideAxisRect.axis(QCPAxis.atBottom), wideAxisRect.axis(QCPAxis.atLeft, 1))
    mainGraphGauss.setData(dataGaussX, dataGaussY)
    mainGraphGauss.setPen(QPen(QColor("#8070B8"), 2))
    mainGraphGauss.setBrush(QColor(110, 170, 110, 30))
    mainGraphCos.setChannelFillGraph(mainGraphGauss)
    mainGraphCos.setBrush(QColor(255, 161, 0, 50))
    mainGraphGauss.valueAxis().setRange(0, 1000)
    mainGraphGauss.rescaleKeyAxis()

    subGraphRandom = customPlot.addGraph(subRectLeft.axis(QCPAxis.atBottom), subRectLeft.axis(QCPAxis.atLeft))
    subGraphRandom.setData(dataRandomX, dataRandomY)
    subGraphRandom.setLineStyle(QCPGraph.lsImpulse)
    subGraphRandom.setPen(QPen(QColor("#FFA100"), 1.5))
    subGraphRandom.valueAxis().setRange(-rInt,rInt)
    subGraphRandom.rescaleKeyAxis()

    subBars = QCPBars(subRectRight.axis(QCPAxis.atBottom), subRectRight.axis(QCPAxis.atRight))
    subBars.setWidth(3.0/float(len(x3)))
    subBars.setData(x3, y3)
    subBars.setPen(QPen(Qt.black))
    subBars.setAntialiased(False)
    subBars.setAntialiasedFill(False)
    subBars.setBrush(QColor("#705BE8"))
    subBars.keyAxis().setSubTicks(False)
    subBars.rescaleAxes()

    # setup a ticker for subBars key axis that only gives integer ticks:
    intTicker = QCPAxisTickerFixed()
    intTicker.setTickStep(1.0)
    intTicker.setScaleStrategy(QCPAxisTickerFixed.ssMultiples)
    subBars.keyAxis().setTicker(intTicker)



   # customPlot.rescaleAxes()
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




