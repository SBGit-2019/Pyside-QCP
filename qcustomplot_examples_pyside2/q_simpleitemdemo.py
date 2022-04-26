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
    customPlot.setWindowTitle('Simple Item Demo')

    customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom)

    # add the text label at the top:
    textLabel = QCPItemText(customPlot)
    textLabel.setPositionAlignment(Qt.AlignTop|Qt.AlignHCenter)
    textLabel.position().setType(QCPItemPosition.ptAxisRectRatio)
    textLabel.position().setCoords(0.5, 0) # place position at center/top of axis rect
    textLabel.setText("Text Item Demo")
    textLabel.setFont(QFont(QtGui.QFont().family(), 16)) # make font a bit larger
    textLabel.setPen(QPen(Qt.black)) # show black border around text

    # add the arrow:
    arrow = QCPItemLine(customPlot)
    arrow.start().setParentAnchor(textLabel.bottom())
    arrow.end().setCoords(4, 1.6) # point to (4, 1.6) in x-y-plot coordinates
    spike = QCPLineEnding(QCPLineEnding.esSpikeArrow)
    arrow.setHead(spike)

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



