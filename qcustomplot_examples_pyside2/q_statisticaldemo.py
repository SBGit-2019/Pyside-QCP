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
    customPlot.setWindowTitle('Statistical Demo')

    statistical = QCPStatisticalBox(customPlot.xAxis, customPlot.yAxis)
    boxBrush = QBrush(QColor(60, 60, 255, 100))
    boxBrush.setStyle(Qt.Dense6Pattern) # make it look oldschool
    statistical.setBrush(boxBrush)

    # specify data:
    statistical.addData(1, 1.1, 1.9, 2.25, 2.7, 4.2)
    vec1 = [ 0.7 , 0.34 , 0.45 , 6.2 , 5.8] # provide some outliers as QVector
    statistical.addData(2, 0.8, 1.6, 2.2, 3.2, 4.9, vec1)
    statistical.addData(3, 0.2, 0.7, 1.1, 1.6, 2.9)

    # Check data access
    data = statistical.data()
    statistical.setData(data[0], data[1], data[2], data[3], data[4], data[5])

    # prepare manual x axis labels:
    customPlot.xAxis.setSubTicks(False)
    customPlot.xAxis.setTickLength(0, 4)
    customPlot.xAxis.setTickLabelRotation(20)
    textTicker = QCPAxisTickerText()
    textTicker.addTick(1, "Sample 1")
    textTicker.addTick(2, "Sample 2")
    textTicker.addTick(3, "Control Group")
    customPlot.xAxis.setTicker(textTicker)

    # prepare axes:
    customPlot.yAxis.setLabel("O₂ Absorption [mg]")
    customPlot.rescaleAxes()
    customPlot.xAxis.scaleRange(1.7, customPlot.xAxis.range().center())
    customPlot.yAxis.setRange(0, 7)
    customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom)


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



