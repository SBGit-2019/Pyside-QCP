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
import shiboken2 as Shiboken


def demo(app, demotime=0):
    customPlot = QCustomPlot()
    screen = QGuiApplication.primaryScreen().geometry()
    customPlot.resize(screen.height(), screen.height()*0.75)
    customPlot.setWindowTitle('Line Style Demo')

    customPlot.legend.setVisible(True)
    customPlot.legend.setFont(QFont("Helvetica", 9))
    pen = QPen()
    lineNames = ["lsNone", "lsLine", "lsStepLeft", "lsStepRight", "lsStepCenter", "lsImpulse"]
    # add graphs with different line styles:
    for i in range(QCPGraph.lsNone, QCPGraph.lsImpulse + 1):
      customPlot.addGraph()
      pen.setColor(QColor(math.sin(i*1+1.2)*80+80, math.sin(i*0.3+0)*80+80, math.sin(i*0.3+1.5)*80+80))
      customPlot.graph().setPen(pen)
      customPlot.graph().setName(lineNames[i-QCPGraph.lsNone])
      customPlot.graph().setLineStyle(QCPGraph.LineStyle(i))
      customPlot.graph().setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssCircle, 5))
      # generate data:
      x = [0.0] * 15
      y = [0.0] * 15
      for j in range(0, 15):
        x[j] = j/15.0 * 5*3.14 + 0.01
        y[j] = 7*math.sin(x[j])/x[j] - (i-QCPGraph.lsNone)*5 + (QCPGraph.lsImpulse)*5 + 2

      customPlot.graph().setData(x, y)
      customPlot.graph().rescaleAxes(True)

    # zoom out a bit:
    customPlot.yAxis.scaleRange(1.1, customPlot.yAxis.range().center())
    customPlot.xAxis.scaleRange(1.1, customPlot.xAxis.range().center())
    # set blank axis lines:
    customPlot.xAxis.setTicks(False)
    customPlot.yAxis.setTicks(True)
    customPlot.xAxis.setTickLabels(False)
    customPlot.yAxis.setTickLabels(True)
    # make top right axes clones of bottom left axes:
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






