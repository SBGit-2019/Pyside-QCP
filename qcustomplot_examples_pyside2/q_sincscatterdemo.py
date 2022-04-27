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
    customPlot.setWindowTitle('Sinc Scatter Demo')

    customPlot.legend.setVisible(True)
    customPlot.legend.setFont(QFont("Helvetica",9))
    # set locale to english, so we get english decimal separator:
    customPlot.setLocale(QLocale(QLocale.English, QLocale.UnitedKingdom))

    # add confidence band graphs:
    customPlot.addGraph();
    pen = QPen()
    pen.setStyle(Qt.DotLine)
    pen.setWidth(1)
    pen.setColor(QColor(180,180,180))
    customPlot.graph(0).setName("Confidence Band 68%")
    customPlot.graph(0).setPen(pen)
    customPlot.graph(0).setBrush(QBrush(QColor(255,50,30,20)))
    customPlot.addGraph()
    customPlot.legend.removeItem(customPlot.legend.itemCount()-1)
    customPlot.graph(1).setPen(pen)
    customPlot.graph(0).setChannelFillGraph(customPlot.graph(1))
    # add theory curve graph:
    customPlot.addGraph()
    pen.setStyle(Qt.DashLine)
    pen.setWidth(2)
    pen.setColor(Qt.red)
    customPlot.graph(2).setPen(pen)
    customPlot.graph(2).setName("Theory Curve")
    # add data point graph:
    customPlot.addGraph()
    customPlot.graph(3).setPen(QPen(Qt.blue))
    customPlot.graph(3).setLineStyle(QCPGraph.lsNone)
    customPlot.graph(3).setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCross, 4))
    # add error bars:
    errorBars = QCPErrorBars(customPlot.xAxis, customPlot.yAxis)
    errorBars.removeFromLegend()
    errorBars.setAntialiased(False)
    errorBars.setDataPlottable(customPlot.graph(3))
    errorBars.setPen(QPen(QColor(180,180,180)))
    customPlot.graph(3).setName("Measurement")

    # generate ideal sinc curve data and some randomly perturbed data for scatter plot:
    #x0 = [(0.0,0.0)] * 250
    x0 = [0.0] * 250
    y0 = [0.0] * 250
    yConfUpper = [0.0] * 250
    yConfLower = [0.0] * 250
    for i in range(0, 250):
      x0[i] = (i/249.0-0.5)*30+0.01 # by adding a small offset we make sure not do divide by zero in next code line
      y0[i] = math.sin(x0[i])/x0[i] # sinc function
      yConfUpper[i] = y0[i]+0.15
      yConfLower[i] = y0[i]-0.15
      x0[i] *= 1000
      # x0[i]=(i,i)
    #list1, list2 = zip(*x0)


    x1 = [0.0] * 50
    y1 = [0.0] * 50
    y1err = [0.0] * 50
    for i in range(0, 50):
      # generate a gaussian distributed random number:
      tmp1 = uniform(0.0,1.0)
      tmp2 = uniform(0.0,1.0)
      r = math.sqrt(-2.0*math.log(tmp1))*math.cos(2*math.pi*tmp2) # box-muller transform for gaussian distribution
      # set y1 to value of y0 plus a random gaussian pertubation:
      x1[i] = (float(i)/50.0-0.5)*30+0.25
      y1[i] = math.sin(x1[i])/x1[i]+r*0.15
      x1[i] *= 1000
      y1err[i] = 0.15

    # pass data to graphs and let QCustomPlot determine the axes ranges so the whole thing is visible:
    customPlot.graph(0).setData(x0, yConfUpper)
    customPlot.graph(1).setData(x0, yConfLower)
    customPlot.graph(2).setData(x0, y0)
    customPlot.graph(3).setData(x1, y1)

    # Check direct data access
    grph =  customPlot.graph(0)
    data = grph.data()
    container = grph.dataContainer()
    grph.setData(container)
    grph.setData(data[0],data[1])

    errorBars.setData(y1err)
    # Try change of data
    errorDatas = errorBars.data()
    errorDatasMinus = [x-0.05 for x in errorDatas[0]]
    errorDatasPlus = [x-0.02 for x in errorDatas[1]]
    errorBars.setData(errorDatasMinus,errorDatasPlus)

    customPlot.graph(2).rescaleAxes()
    customPlot.graph(3).rescaleAxes(True)
    # setup look of bottom tick labels:
    xAxis = customPlot.xAxis
    xAxis.setTickLabelRotation(30)
    xAxis.ticker().setTickCount(9)
    xAxis.setNumberFormat("ebc")
    xAxis.setNumberPrecision(1)
    xAxis.moveRange(-10)
    # make top right axes clones of bottom left axes. Looks prettier:
    customPlot.axisRect().setupFullAxesBox()


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



