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
    customPlot.setWindowTitle('Bar Chart Demo')

    # set dark background gradient:
    gradient = QLinearGradient(0, 0, 0, 400)
    gradient.setColorAt(0, QColor(90, 90, 90))
    gradient.setColorAt(0.38, QColor(105, 105, 105))
    gradient.setColorAt(1, QColor(70, 70, 70))
    customPlot.setBackground(QBrush(gradient))

    # create empty bar chart objects:
    regen = QCPBars(customPlot.xAxis, customPlot.yAxis)
    nuclear = QCPBars(customPlot.xAxis, customPlot.yAxis)
    fossil = QCPBars(customPlot.xAxis, customPlot.yAxis)
    regen.setAntialiased(False) # gives more crisp, pixel aligned bar borders
    nuclear.setAntialiased(False)
    fossil.setAntialiased(False)
    regen.setStackingGap(1)
    nuclear.setStackingGap(1)
    fossil.setStackingGap(1)
    # set names and colors:
    fossil.setName("Fossil fuels")
    fossil.setPen(QPen(QColor(111, 9, 176).lighter(170)))
    fossil.setBrush(QColor(111, 9, 176))
    nuclear.setName("Nuclear")
    nuclear.setPen(QPen(QColor(250, 170, 20).lighter(150)))
    nuclear.setBrush(QColor(250, 170, 20))
    regen.setName("Regenerative")
    regen.setPen(QPen(QColor(0, 168, 140).lighter(130)))
    regen.setBrush(QColor(0, 168, 140))
    # stack bars on top of each other:
    nuclear.moveAbove(fossil)
    regen.moveAbove(nuclear)

    # prepare x axis with country labels:
    xAxis = customPlot.xAxis
    gridX = xAxis.grid()
    ticks = [1, 2, 3, 4, 5, 6, 7]
    labels = ["USA", "Japan", "Germany", "France", "UK", "Italy", "Canada"]
    textTicker = QCPAxisTickerText()
    textTicker.addTicks(ticks, labels)
    customPlot.xAxis.setTicker(textTicker)
    customPlot.xAxis.setTickLabelRotation(60)
    customPlot.xAxis.setSubTicks(False)
    customPlot.xAxis.setTickLength(0, 4)
    customPlot.xAxis.setRange(0, 8)
    customPlot.xAxis.setBasePen(QPen(Qt.white))
    customPlot.xAxis.setTickPen(QPen(Qt.white))
    gridX.setVisible(True)
    gridX.setPen(QPen(QColor(130, 130, 130), 0, Qt.DotLine))
    customPlot.xAxis.setTickLabelColor(Qt.white)
    customPlot.xAxis.setLabelColor(Qt.white)

    # prepare y axis:
    yAxis = customPlot.yAxis
    gridY = yAxis.grid()
    customPlot.yAxis.setRange(0, 12.1)
    customPlot.yAxis.setPadding(5) # a bit more space to the left border
    customPlot.yAxis.setLabel("Power Consumption in\nKilowatts per Capita (2007)")
    customPlot.yAxis.setBasePen(QPen(Qt.white))
    customPlot.yAxis.setTickPen(QPen(Qt.white))
    customPlot.yAxis.setSubTickPen(QPen(Qt.white))
    gridY.setSubGridVisible(True)
    customPlot.yAxis.setTickLabelColor(Qt.white)
    customPlot.yAxis.setLabelColor(Qt.white)
    gridY.setPen(QPen(QColor(130, 130, 130), 0, Qt.SolidLine))
    gridY.setSubGridPen(QPen(QColor(130, 130, 130), 0, Qt.DotLine))

    # Add data:
    fossilData = [0.86*10.5, 0.83*5.5, 0.84*5.5, 0.52*5.8, 0.89*5.2, 0.90*4.2, 0.67*11.2]
    nuclearData = [0.08*10.5, 0.12*5.5, 0.12*5.5, 0.40*5.8, 0.09*5.2, 0.00*4.2, 0.07*11.2]
    regenData = [0.06*10.5, 0.05*5.5, 0.04*5.5, 0.06*5.8, 0.02*5.2, 0.07*4.2, 0.25*11.2]
    fossil.setData(ticks, fossilData)
    nuclear.setData(ticks, nuclearData)
    regen.setData(ticks, regenData)

    # setup legend:
    customPlot.legend.setVisible(True)
    customPlot.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignTop|Qt.AlignHCenter)
    customPlot.legend.setBrush(QColor(255, 255, 255, 100))
    customPlot.legend.setBorderPen(Qt.NoPen)
    legendFont = QtGui.QFont()
    legendFont.setPointSize(10)
    customPlot.legend.setFont(legendFont)
    customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom)


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





