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
    customPlot.setWindowTitle('Financial Charts Demo')

    customPlot.legend.setVisible(True)

    # generate two sets of random walk data (one for candlestick and one for ohlc chart):
    n = 500
    time = [0.0]*n
    value1 = [0.0]*n
    value2 = [0.0]*n
    start = QDateTime(QDate(2014, 6, 11))
    start.setTimeSpec(Qt.UTC)
    startTime = start.toTime_t()
    binSize = 3600*24 # bin data in 1 day intervals
    time[0] = startTime
    value1[0] = 60
    value2[0] = 20
    for i in range(1, n):
      time[i] = startTime + 3600*i
      value1[i] = value1[i-1] + (uniform(0.0,1.0)-0.5)*10
      value2[i] = value2[i-1] + (uniform(0.0,1.0)-0.5)*3

    # create candlestick chart:
    candlesticks = QCPFinancial(customPlot.xAxis, customPlot.yAxis)
    candlesticks.setName("Candlestick")
    candlesticks.setChartStyle(QCPFinancial.csCandlestick)
    fdata = QCPFinancial.timeSeriesToOhlc(time, value1, binSize, startTime)
    candlesticks.setData(fdata)
    candlesticks.setWidth(binSize*0.9)
    candlesticks.setTwoColored(True)
    candlesticks.setBrushPositive(QColor(245, 245, 245))
    candlesticks.setBrushNegative(QColor(40, 40, 40))
    candlesticks.setPenPositive(QPen(QColor(0, 0, 0)))
    candlesticks.setPenNegative(QPen(QColor(0, 0, 0)))
    data =  candlesticks.data()
    candlesticks.setData(data[0], data[1], data[2], data[3], data[4])

    # create ohlc chart:
    ohlc = QCPFinancial(customPlot.xAxis, customPlot.yAxis)
    ohlc.setName("OHLC")
    ohlc.setChartStyle(QCPFinancial.csOhlc)
    fdata2=QCPFinancial.timeSeriesToOhlc(time, value2, binSize/3.0, startTime)
    ohlc.setData(fdata2) # divide binSize by 3 just to make the ohlc bars a bit denser
    ohlc.setWidth(binSize*0.2)
    ohlc.setTwoColored(True)

    # create bottom axis rect for volume bar chart:
    QWIDGETSIZE_MAX = (1 << 24) - 1 # ToDo: QWIDGETSIZE_MAX is not defined in PySide2?
    volumeAxisRect = QCPAxisRect(customPlot)
    customPlot.plotLayout().addElement(1, 0, volumeAxisRect)
    volumeAxisRect.setMaximumSize(QSize(QWIDGETSIZE_MAX, 100))
    volumeAxisRect.axis(QCPAxis.atBottom).setLayer("axes")
    volumeAxisRect.axis(QCPAxis.atBottom).grid().setLayer("grid")
    # bring bottom and main axis rect closer together:
    customPlot.plotLayout().setRowSpacing(0)
    volumeAxisRect.setAutoMargins(QCP.msLeft|QCP.msRight|QCP.msBottom)
    volumeAxisRect.setMargins(QMargins(0, 0, 0, 0))
    # create two bar plottables, for positive (green) and negative (red) volume bars:
    customPlot.setAutoAddPlottableToLegend(False)
    volumePos = QCPBars(volumeAxisRect.axis(QCPAxis.atBottom), volumeAxisRect.axis(QCPAxis.atLeft))
    volumeNeg = QCPBars(volumeAxisRect.axis(QCPAxis.atBottom), volumeAxisRect.axis(QCPAxis.atLeft))
    for i in range(0, int(n/5)):
      v = uniform(0.0,20000.0)+uniform(0.0,20000.0)+uniform(0.0,20000.0)-10000*3
      if v < 0: # add data to either volumeNeg or volumePos, depending on sign of v
        volumeNeg.addData(startTime+3600*5.0*i, math.fabs(v))
      else:
        volumePos.addData(startTime+3600*5.0*i, math.fabs(v))

    volumePos.setWidth(3600*4)
    volumePos.setPen(Qt.NoPen)
    volumePos.setBrush(QColor(100, 180, 110))
    volumeNeg.setWidth(3600*4)
    volumeNeg.setPen(Qt.NoPen)
    volumeNeg.setBrush(QColor(180, 90, 90))

    data = volumePos.data()
    volumePos.setData(data[0], data[1])

    # interconnect x axis ranges of main and bottom axis rects:
    customPlot.xAxis.rangeChanged.connect(volumeAxisRect.axis(QCPAxis.atBottom).setRange)
    volumeAxisRect.axis(QCPAxis.atBottom).rangeChanged.connect(customPlot.xAxis.setRange)

    # configure axes of both main and bottom axis rect:
    dateTimeTicker = QCPAxisTickerDateTime()
    dateTimeTicker.setDateTimeSpec(Qt.UTC)
    dateTimeTicker.setDateTimeFormat("dd. MMMM")
    volumeAxisRect.axis(QCPAxis.atBottom).setTicker(dateTimeTicker)
    volumeAxisRect.axis(QCPAxis.atBottom).setTickLabelRotation(15)
    customPlot.xAxis.setBasePen(Qt.NoPen)
    customPlot.xAxis.setTickLabels(False)
    customPlot.xAxis.setTicks(False) # only want vertical grid in main axis rect, so hide xAxis backbone, ticks, and labels
    dateTimeTicker2 = QCPAxisTickerDateTime()
    dateTimeTicker2.setDateTimeSpec(Qt.UTC)
    dateTimeTicker2.setDateTimeFormat("dd. MMMM")
    customPlot.xAxis.setTicker(dateTimeTicker2)
    customPlot.rescaleAxes()
    customPlot.xAxis.scaleRange(1.025, customPlot.xAxis.range().center())
    customPlot.yAxis.scaleRange(1.1, customPlot.yAxis.range().center())

    # make axis rects' left side line up:
    group = QCPMarginGroup(customPlot)
    customPlot.axisRect().setMarginGroup(QCP.msLeft|QCP.msRight, group)
    volumeAxisRect.setMarginGroup(QCP.msLeft|QCP.msRight, group)

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
