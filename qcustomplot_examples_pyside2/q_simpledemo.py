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
from PySide2 import QtGui,QtCore
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
    customPlot.setWindowTitle('Simple Demo')


    # add two new graphs and set their look:
    customPlot.addGraph()
    customPlot.graph(0).setPen(QPen(Qt.blue)) # line color blue for first graph
    customPlot.graph(0).setBrush(QBrush(QColor(0, 0, 255, 20))) # first graph will be filled with translucent blue
    customPlot.addGraph()
    customPlot.graph(1).setPen(QPen(Qt.red)) # line color red for second graph
    # generate some points of data (y0 for first, y1 for second graph):
    x = [0.0] * 251
    y0 = [0.0] * 251
    y1 = [0.0] * 251
    for i in range(0,251):
      x[i] = i
      y0[i] = math.exp(-i/150.0)*math.cos(i/10.0) # exponentially decaying cosine
      y1[i] = math.exp(-i/150.0)              # exponential envelope

    # configure right and top axis to show ticks but no labels:
    # (see QCPAxisRect::setupFullAxesBox for a quicker method to do this)
    customPlot.xAxis2.setVisible(True)
    customPlot.xAxis2.setTickLabels(False)
    customPlot.yAxis2.setVisible(True)
    customPlot.yAxis2.setTickLabels(False)
    # make left and bottom axes always transfer their ranges to right and top axes:
    customPlot.xAxis.rangeChanged.connect(customPlot.xAxis2.setRange)
    customPlot.yAxis.rangeChanged.connect(customPlot.yAxis2.setRange)
    # pass data points to graphs:
    customPlot.graph(0).setData(x, y0)
    customPlot.graph(1).setData(x, y1)
    # let the ranges scale themselves so graph 0 fits perfectly in the visible area:
    customPlot.graph(0).rescaleAxes()
    # same thing for graph 1, but only enlarge ranges (in case graph 1 is smaller than graph 0):
    customPlot.graph(1).rescaleAxes(True)
    # Note: we could have also just called customPlot.rescaleAxes() instead
    # Allow user to drag axis ranges with mouse, zoom with mouse wheel and select graphs by clicking:
    customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectPlottables)



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




