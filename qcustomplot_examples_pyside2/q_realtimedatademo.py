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

time = QTime.currentTime()
lastPointKey = 0
customPlot = None
lastFpsKey = 0.0
frameCount = 0

def realtimeDataSlot(): # called by timer
    # calculate two new data points:
    global lastPointKey
    global time
    global customPlot
    global lastFpsKey
    global frameCount
    key = time.elapsed()/1000.0 # time elapsed since start of demo, in seconds

    if key-lastPointKey > 0.002: # at most add point every 2 ms
      # add data to lines:
      customPlot.graph(0).addData(key, math.sin(key)+uniform(0,1)*1.0*math.sin(key/0.3843))
      customPlot.graph(1).addData(key, math.cos(key)+uniform(0,1)*0.5*math.sin(key/0.4364))
      # rescale value (vertical) axis to fit the current data:
      lastPointKey = key;

    # make key axis range scroll with the data (at a constant range size of 8):
    customPlot.xAxis.setRange(key, 8, Qt.AlignRight)
    customPlot.replot();

    # calculate frames per second:
    frameCount += 1

    if key-lastFpsKey > 2:  # average fps over 2 seconds
      fps = float(frameCount)/(float)(key-lastFpsKey)
      sz = customPlot.graph(0).dataCount()+customPlot.graph(1).dataCount()
      fps_str = '{:3.2f}'.format(fps)
      customPlot.setWindowTitle('Real Time Data Demo FPS: '+fps_str+" Data:"+str(sz))
      lastFpsKey = key
      frameCount = 0




def demo(app, demotime=0):
    global lastPointKey
    global time
    global customPlot
    global lastFpsKey
    global frameCount
    customPlot = QCustomPlot()
    screen = QGuiApplication.primaryScreen().geometry()
    customPlot.resize(screen.height(), screen.height()*0.75)
    customPlot.setWindowTitle('Real Time Data Demo')

    customPlot.addGraph() # blue line
    customPlot.graph(0).setPen(QPen(QColor(40, 110, 255)))
    customPlot.addGraph() # red line
    customPlot.graph(1).setPen(QPen(QColor(255, 110, 40)))

    timeTicker = QCPAxisTickerTime()
    timeTicker.setTimeFormat("%h:%m:%s")
    customPlot.xAxis.setTicker(timeTicker)
    customPlot.axisRect().setupFullAxesBox()
    customPlot.yAxis.setRange(-1.2, 1.2)

    # make left and bottom axes transfer their ranges to right and top axes:
    customPlot.xAxis.rangeChanged.connect(customPlot.xAxis2.setRange)
    customPlot.yAxis.rangeChanged.connect(customPlot.yAxis2.setRange)

    # setup a timer that repeatedly calls MainWindow::realtimeDataSlot:
    dataTimer = QTimer()
    dataTimer.timeout.connect(realtimeDataSlot)
    dataTimer.start(0)


    closeTimer = QTimer()
    closeTimer.timeout.connect(customPlot.close)
    if demotime > 0:
        closeTimer.start(demotime)
    customPlot.show()


    # Create and show the form
    # Run the main Qt loop
    res = app.exec_()
    del dataTimer

    customPlot = None
    return res


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    res = demo(app)
    sys.exit(res)


