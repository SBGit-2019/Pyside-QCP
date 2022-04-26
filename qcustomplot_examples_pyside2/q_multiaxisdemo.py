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
    customPlot.setWindowTitle('Multi Axis Demo')

    our_package_dir = os.path.abspath(os.path.dirname(__file__))+"/"


    customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom)

    customPlot.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom)) # period as decimal separator and comma as thousand separator
    customPlot.legend.setVisible(True)
    legendFont = QFont()
    legendFont = QtGui.QFont() # start out with MainWindow's font..
    legendFont.setPointSize(9) # and make a bit smaller for legend
    customPlot.legend.setFont(legendFont)
    customPlot.legend.setBrush(QBrush(QColor(255,255,255,230)))
    # by default, the legend is in the inset layout of the main axis rect. So this is how we access it to change legend placement:
    customPlot.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignBottom|Qt.AlignRight)

    # setup for graph 0: key axis left, value axis bottom
    # will contain left maxwell-like function
    customPlot.addGraph(customPlot.yAxis, customPlot.xAxis)
    customPlot.graph(0).setPen(QPen(QColor(255, 100, 0)))
    customPlot.graph(0).setBrush(QBrush(QPixmap(our_package_dir+"/balboa.jpg"))) # fill with texture of specified image
    customPlot.graph(0).setLineStyle(QCPGraph.lsLine)
    customPlot.graph(0).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssDisc, 5))
    customPlot.graph(0).setName("Left maxwell function")

    # setup for graph 1: key axis bottom, value axis left (those are the default axes)
    # will contain bottom maxwell-like function with error bars
    customPlot.addGraph()
    customPlot.graph(1).setPen(QPen(Qt.red))
    customPlot.graph(1).setBrush(QBrush(QPixmap(our_package_dir+"/balboa.jpg"))) # same fill as we used for graph 0
    customPlot.graph(1).setLineStyle(QCPGraph.lsStepCenter)
    # TODO scatterStyle = QCPScatterStyle(QCPScatterStyle.ssCircle,Qt.red,Qt.white,7.0)
    # BUg in shiboken function generator. jumps in wrong constructor
    scatterStyle = QCPScatterStyle(QCPScatterStyle.ssCircle,7.0)
    scatterStyle.setPen(QPen(Qt.red))
    scatterStyle.setBrush(QBrush(Qt.white))
    customPlot.graph(1).setScatterStyle(scatterStyle) #  Qt.red, Qt.white,
    customPlot.graph(1).setName("Bottom maxwell function")
    errorBars = QCPErrorBars(customPlot.xAxis, customPlot.yAxis)
    errorBars.removeFromLegend()
    errorBars.setDataPlottable(customPlot.graph(1))

    # setup for graph 2: key axis top, value axis right
    # will contain high frequency sine with low frequency beating:
    customPlot.addGraph(customPlot.xAxis2, customPlot.yAxis2)
    customPlot.graph(2).setPen(QPen(Qt.blue))
    customPlot.graph(2).setName("High frequency sine")

    # setup for graph 3: same axes as graph 2
    # will contain low frequency beating envelope of graph 2
    customPlot.addGraph(customPlot.xAxis2, customPlot.yAxis2)
    blueDotPen = QPen()
    blueDotPen.setColor(QColor(30, 40, 255, 150))
    blueDotPen.setStyle(Qt.DotLine)
    blueDotPen.setWidthF(4)
    customPlot.graph(3).setPen(blueDotPen)
    customPlot.graph(3).setName("Sine envelope")

    # setup for graph 4: key axis right, value axis top
    # will contain parabolically distributed data points with some random perturbance
    customPlot.addGraph(customPlot.yAxis2, customPlot.xAxis2)
    customPlot.graph(4).setPen(QColor(50, 50, 50, 255))
    customPlot.graph(4).setLineStyle(QCPGraph.lsNone)
    customPlot.graph(4).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, 4))
    customPlot.graph(4).setName("Some random data around\na quadratic function")

    # generate data, just playing with numbers, not much to learn here:
    x0 = [0.0] * 25
    y0 = [0.0] * 25
    x1 = [0.0] * 15
    y1 = [0.0] * 15
    y1err = [0.0] * 15
    x2 = [0.0] * 250
    y2 = [0.0] * 250
    x3 = [0.0] * 250
    y3 = [0.0] * 250
    x4 = [0.0] * 250
    y4 = [0.0] * 250

    for i in range(0, 25): # data for graph 0
      x0[i] = 3*i/25.0
      y0[i] = math.exp(-x0[i]*x0[i]*0.8)*(x0[i]*x0[i]+x0[i])

    for i in range(0, 15): # data for graph 1
      x1[i] = 3*i/15.0
      y1[i] = math.exp(-x1[i]*x1[i])*(x1[i]*x1[i])*2.6
      y1err[i] = y1[i]*0.25

    for i in range(0, 250): # data for graphs 2, 3 and 4
      x2[i] = i/250.0*3*math.pi
      x3[i] = x2[i]
      x4[i] = i/250.0*100-50
      y2[i] = math.sin(x2[i]*12)*math.cos(x2[i])*10
      y3[i] = math.cos(x3[i])*10
      y4[i] = 0.01*x4[i]*x4[i] + 1.5*(uniform(0.0,1.0)-0.5) + 1.5*math.pi


    # pass data points to graphs:
    customPlot.graph(0).setData(x0, y0)
    customPlot.graph(1).setData(x1, y1)
    errorBars.setData(y1err)
    customPlot.graph(2).setData(x2, y2)
    customPlot.graph(3).setData(x3, y3)
    customPlot.graph(4).setData(x4, y4)
    # activate top and right axes, which are invisible by default:
    customPlot.xAxis2.setVisible(True)
    customPlot.yAxis2.setVisible(True)
    # set ranges appropriate to show data:
    customPlot.xAxis.setRange(0, 2.7)
    customPlot.yAxis.setRange(0, 2.6)
    customPlot.xAxis2.setRange(0, 3.0*math.pi)
    customPlot.yAxis2.setRange(-70, 35)
    # set pi ticks on top axis:
    ticker=QCPAxisTickerPi()
    customPlot.xAxis2.setTicker(ticker)
    # add title layout element:
    customPlot.plotLayout().insertRow(0)
    # customPlot.plotLayout().setRowStretchFactor(0,0.1)
    text = QCPTextElement(customPlot, "Way too many graphs in one plot", QFont("sans", 12, QFont.Bold))
    text.setTextColor(Qt.blue)
    customPlot.plotLayout().addElement(0, 0, text)
    # set labels:
    customPlot.xAxis.setLabel("Bottom axis with outward ticks")
    customPlot.yAxis.setLabel("Left axis label")
    customPlot.xAxis2.setLabel("Top axis label")
    customPlot.yAxis2.setLabel("Right axis label")
    # make ticks on bottom axis go outward:
    customPlot.xAxis.setTickLength(0, 5)
    customPlot.xAxis.setSubTickLength(0, 3)
    # make ticks on right axis go inward and outward:
    customPlot.yAxis2.setTickLength(3, 3)
    customPlot.yAxis2.setSubTickLength(1, 1)


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



