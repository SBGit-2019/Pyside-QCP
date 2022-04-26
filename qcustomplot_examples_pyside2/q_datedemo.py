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
    customPlot.setWindowTitle('Date Demo')

    # set locale to english, so we get english month names:
    customPlot.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))
    # seconds of current time, we'll use it as starting point in time for data:
    now = QDateTime.currentDateTime().toTime_t()
    # create multiple graphs:
    for gi in range(0, 5):
      customPlot.addGraph()
      color = QColor(20+200/4.0*gi,70*(1.6-gi/4.0), 150, 150)
      customPlot.graph().setLineStyle(QCPGraph.lsLine)
      customPlot.graph().setPen(QPen(color.lighter(200)))
      customPlot.graph().setBrush(QBrush(color))
      timeDataX = [0.0] * 250
      timeDataY = [0.0] * 250
      # generate random walk data:
      for i in range(0,250) :
        timeDataX[i] =now + 24*3600*i
        if i == 0:
          timeDataY[i]= (float(i)/50.0+1)*uniform(-0.5,0.5)
        else:
          timeDataY[i]= math.fabs(timeDataY[i-1])*(1+0.02/4.0*(4-gi)) + (float(i)/50.0+1)*uniform(-0.5,0.5)
      customPlot.graph().setData(timeDataX, timeDataY)

    dateTicker=QCPAxisTickerDateTime()
    dateTicker.setDateTimeFormat("d. MMMM\nyyyy")
    customPlot.xAxis.setTicker(dateTicker)

    # configure left axis text labels:
    textTicker=QCPAxisTickerText()
    textTicker.addTick(10, "a bit\nlow")
    textTicker.addTick(50, "quite\nhigh")
    customPlot.yAxis.setTicker(textTicker)

   #textTicker = QCPAxisTickerText()
   #textTicker.addTick(1, "Sample 1")
   #textTicker.addTick(2, "Sample 2")
   #textTicker.addTick(3, "Control Group")
   #customPlot.xAxis.setTicker(textTicker)

    # set a more compact font size for bottom and left axis tick labels:
    customPlot.xAxis.setTickLabelFont(QFont(QFont().family(), 8))
    customPlot.yAxis.setTickLabelFont(QFont(QFont().family(), 8))

    # set axis labels:
    customPlot.xAxis.setLabel("Date")
    customPlot.yAxis.setLabel("Random wobbly lines value")

    # make top and right axes visible but without ticks and labels:
    customPlot.xAxis2.setVisible(True)
    customPlot.yAxis2.setVisible(True)
    customPlot.xAxis2.setTicks(False)
    customPlot.yAxis2.setTicks(False)
    customPlot.xAxis2.setTickLabels(False)
    customPlot.yAxis2.setTickLabels(False)

    # set axis ranges to show all data:
    customPlot.xAxis.setRange(now, now+24*3600*249)
    customPlot.yAxis.setRange(0, 60)
    # show legend with slightly transparent background brush:
    customPlot.legend.setVisible(True)
    customPlot.legend.setBrush(QColor(255, 255, 255, 150))



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



