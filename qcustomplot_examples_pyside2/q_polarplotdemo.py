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
    customPlot.setWindowTitle('Polarplot Demo')
    customPlot.plotLayout().clear()


    angularAxis = QCPPolarAxisAngular(customPlot)
    customPlot.plotLayout().addElement(0, 0, angularAxis);

    customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom)
    angularAxis.setRangeDrag(False)
    angularAxis.setTickLabelMode(QCPPolarAxisAngular.lmUpright)

    angularAxis.radialAxis().setTickLabelMode(QCPPolarAxisRadial.lmUpright)
    angularAxis.radialAxis().setTickLabelRotation(0)
    angularAxis.radialAxis().setAngle(45)

    angularAxis.grid().setAngularPen(QPen(QColor(200, 200, 200), 0, Qt.SolidLine))
    angularAxis.grid().setSubGridType(QCPPolarGrid.gtAll)

    g1 = QCPPolarGraph(angularAxis, angularAxis.radialAxis())
    g2 = QCPPolarGraph(angularAxis, angularAxis.radialAxis())

    g2.setPen(QPen(QColor(255, 150, 20)))
    g2.setBrush(QColor(255, 150, 20, 50))
    g1.setScatterStyle(QCPScatterStyle(QCPScatterStyle.ssDisc))
    for i in range(0,101):
      g1.addData(i/100.0*360.0, math.sin(i/100.0*math.pi*8)*8+1)
      g2.addData(i/100.0*360.0, math.sin(i/100.0*math.pi*6)*2)
    angularAxis.setRange(0, 360)
    angularAxis.radialAxis().setRange(-10, 10)

    # Check data access
    data = g1.data()
    g1.setData(data[0], data[1])

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




