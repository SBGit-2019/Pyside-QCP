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
    customPlot.setWindowTitle('Color Map Demo')
    # configure axis rect:
    customPlot.setInteractions(QCP.iRangeDrag|QCP.iRangeZoom) # this will also allow rescaling the color scale by dragging/zooming
    customPlot.axisRect().setupFullAxesBox(True)
    customPlot.xAxis.setLabel("x")
    customPlot.yAxis.setLabel("y")

    # set up the QCPColorMap:
    colorMap = QCPColorMap(customPlot.xAxis, customPlot.yAxis)
    nx = 200
    ny = 200
    colorMap.data().setSize(nx, ny) # we want the color map to have nx * ny data points
    colorMap.data().setRange(QCPRange(-4, 4), QCPRange(-4, 4)) # and span the coordinate range -4..4 in both key (x) and value (y) dimensions
    # now we assign some data, by accessing the QCPColorMapData instance of the color map:
    for xIndex in range(0, nx):
        for yIndex in range(0, ny):
            aa = colorMap.data().cellToCoord(xIndex, yIndex)
            x = aa[0]
            y = aa[1]
            r = 3.0*math.sqrt(x*x+y*y)+1e-2
            z = 2.0*x*(math.cos(r+2.0)/r-math.sin(r+2.0)/r) # the B field strength of dipole radiation (modulo physical constants)
            colorMap.data().setCell(xIndex, yIndex, z)

    # add a color scale:
    colorScale = QCPColorScale(customPlot)
    customPlot.plotLayout().addElement(0, 1, colorScale) # add it to the right of the main axis rect
    colorScale.setType(QCPAxis.atRight) # scale shall be vertical bar with tick/axis labels right (actually atRight is already the default)
    colorMap.setColorScale(colorScale) # associate the color map with the color scale
    colorScale.axis().setLabel("Magnetic Field Strength")

    # set the color gradient of the color map to one of the presets:
    h1 = QCPColorGradient(QCPColorGradient.gpPolar)
    colorMap.setGradient(h1)
    # we could have also created a QCPColorGradient instance and added own colors to
    # the gradient, see the documentation of QCPColorGradient for what's possible.

    # rescale the data dimension (color) such that all data points lie in the span visualized by the color gradient:
    colorMap.rescaleDataRange();

    # make sure the axis rect and color scale synchronize their bottom and top margins (so they line up):
    marginGroup = QCPMarginGroup(customPlot)
    customPlot.axisRect().setMarginGroup(QCP.msBottom|QCP.msTop, marginGroup)
    colorScale.setMarginGroup(QCP.msBottom|QCP.msTop, marginGroup)

    customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectPlottables)
    customPlot.axisRect().setupFullAxesBox()
    # rescale the key (x) and value (y) axes so the whole color map is visible:
    customPlot.rescaleAxes()

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



