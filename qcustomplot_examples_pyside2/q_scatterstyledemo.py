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
    customPlot.setWindowTitle('Scatter Style Demo')

    customPlot.legend.setVisible(True)
    customPlot.legend.setFont(QFont("Helvetica", 9))
    customPlot.legend.setRowSpacing(-3)
    shapes = [QCPScatterStyle.ssCross, QCPScatterStyle.ssPlus, QCPScatterStyle.ssCircle, QCPScatterStyle.ssDisc, QCPScatterStyle.ssSquare, QCPScatterStyle.ssDiamond, QCPScatterStyle.ssStar, QCPScatterStyle.ssTriangle, QCPScatterStyle.ssTriangleInverted, QCPScatterStyle.ssCrossSquare, QCPScatterStyle.ssPlusSquare, QCPScatterStyle.ssCrossCircle, QCPScatterStyle.ssPlusCircle, QCPScatterStyle.ssPeace, QCPScatterStyle.ssCustom]

    pen = QPen()
    # add graphs with different scatter styles:
    for i in range(0, len(shapes)):
      customPlot.addGraph()
      pen.setColor(QColor(math.sin(i*0.3)*100+100, math.sin(i*0.6+0.7)*100+100, math.sin(i*0.4+0.6)*100+100))
      # generate data:
      x = [0.0] * 10
      y = [0.0] * 10
      for k in range(0, 10):
        x[k] = k/10.0 * 4*3.14 + 0.01
        y[k] = 7*math.sin(x[k])/x[k] + (len(shapes)-i)*5

      customPlot.graph().setData(x, y)
      customPlot.graph().rescaleAxes(True)
      customPlot.graph().setPen(pen)
      #print("dirxx=",dir(QCPScatterStyle.ScatterShape))
      #for key in QCPScatterStyle.ScatterShape.values:
      #    print("KE=",key)
      keyS = (shapes[i].name).decode("utf-8")
      current = QCPScatterStyle.ScatterShape.values[keyS]
      #print("bla=",   shapes[i])
      #print("blak=",   current.name)
      # ToDo: customPlot.graph().setName(QCPScatterStyle.staticMetaObject.enumerator(QCPScatterStyle.staticMetaObject.indexOfEnumerator("ScatterShape")).valueToKey(shapes[i]))
      customPlot.graph().setName(keyS)
      customPlot.graph().setLineStyle(QCPGraph.lsLine)
      # set scatter style:
      if shapes[i] != QCPScatterStyle.ssCustom:
        customPlot.graph().setScatterStyle(QCPScatterStyle(shapes[i], 10))
      else:
        customScatterPath = QPainterPath()
        for i in range(0, 3):
          customScatterPath.cubicTo(math.cos(2*math.pi*i/3.0)*9, math.sin(2*math.pi*i/3.0)*9, math.cos(2*math.pi*(i+0.9)/3.0)*9, math.sin(2*math.pi*(i+0.9)/3.0)*9, 0, 0)
        customPlot.graph().setScatterStyle(QCPScatterStyle(customScatterPath, QPen(Qt.black, 0), QColor(40, 70, 255, 50), 10))

    # set blank axis lines:
    customPlot.rescaleAxes()
    customPlot.xAxis.setTicks(False)
    customPlot.yAxis.setTicks(False)
    customPlot.xAxis.setTickLabels(False)
    customPlot.yAxis.setTickLabels(False)
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

