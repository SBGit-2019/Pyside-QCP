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
    customPlot.setWindowTitle('Texture Brush Demo')

    our_package_dir = os.path.abspath(os.path.dirname(__file__))+"/"

    # add two graphs with a textured fill:
    customPlot.addGraph()
    redDotPen = QPen()
    redDotPen.setStyle(Qt.DotLine)
    redDotPen.setColor(QColor(170, 100, 100, 180))
    redDotPen.setWidthF(2)
    customPlot.graph(0).setPen(redDotPen)
    customPlot.graph(0).setBrush(QBrush(QPixmap(our_package_dir+"/balboa.jpg"))) # fill with texture of specified image

    customPlot.addGraph()
    customPlot.graph(1).setPen(QPen(Qt.red))

    # activate channel fill for graph 0 towards graph 1:
    customPlot.graph(0).setChannelFillGraph(customPlot.graph(1))

    # generate data:
    x = [0.0]*250
    y0 = [0.0]*250
    y1 = [0.0]*250
    for i in range(0, 250):
      # just playing with numbers, not much to learn here
      x[i] = 3*i/250.0
      y0[i] = 1+math.exp(-x[i]*x[i]*0.8)*(x[i]*x[i]+x[i])
      y1[i] = 1-math.exp(-x[i]*x[i]*0.4)*(x[i]*x[i])*0.1

    # pass data points to graphs:
    customPlot.graph(0).setData(x, y0)
    customPlot.graph(1).setData(x, y1)
    # activate top and right axes, which are invisible by default:
    customPlot.xAxis2.setVisible(True)
    customPlot.yAxis2.setVisible(True)
    # make tick labels invisible on top and right axis:
    customPlot.xAxis2.setTickLabels(False)
    customPlot.yAxis2.setTickLabels(False)
    # set ranges:
    customPlot.xAxis.setRange(0, 2.5)
    customPlot.yAxis.setRange(0.9, 1.6)
    # assign top/right axes same properties as bottom/left:
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


