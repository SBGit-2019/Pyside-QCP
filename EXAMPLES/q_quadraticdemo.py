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
from PySide2.QtGui import QLinearGradient, QRadialGradient, QColor, QBrush, QPen, QFont, QPixmap, QPainterPath
from PySide2.QtCore import Qt, QMargins,QPointF,QObject,QCoreApplication,QFile,QTimer,QLocale,QDateTime,QDate,QSize,QTime
from PySide2.QtUiTools import QUiLoader
from qcustomplot import *


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)

    customPlot = QCustomPlot()
    customPlot.resize(800, 600)
    customPlot.setWindowTitle('Quadratic Demo')

    # generate some data:
    x = [0.0] * 101 # initialize with entries 0..100
    y = [0.0] * 101 
    for i in range(0, 101):
      x[i] = i/50.0 - 1 # x goes from -1 to 1
      y[i] = x[i]*x[i]  # let's plot a quadratic function
    
    # create graph and assign data to it:
    customPlot.addGraph()
    customPlot.graph(0).setData(x, y)
    # give the axes some labels:
    customPlot.xAxis.setLabel("x")
    customPlot.yAxis.setLabel("y")
    # set axes ranges, so we see all data:
    customPlot.xAxis.setRange(-1, 1)
    customPlot.yAxis.setRange(0, 1)


    customPlot.show()


    # Create and show the form
    # Run the main Qt loop
    res = app.exec_()
    customPlot = None
    sys.exit(res)



