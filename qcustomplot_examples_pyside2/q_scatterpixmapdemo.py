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
    customPlot.setWindowTitle('Scatter Pixmap Demo')

    our_package_dir = os.path.abspath(os.path.dirname(__file__))+"/"

    customPlot.axisRect().setBackground(QPixmap(our_package_dir+"solarpanels.jpg"))
    customPlot.addGraph()
    customPlot.graph().setLineStyle(QCPGraph.lsLine)

    pen = QPen()
    pen.setColor(QColor(255, 200, 20, 200))
    pen.setStyle(Qt.DashLine)
    pen.setWidthF(2.5)
    customPlot.graph().setPen(pen)
    customPlot.graph().setBrush(QBrush(QColor(255,200,20,70)))
    customPlot.graph().setScatterStyle(QCPScatterStyle(QPixmap(our_package_dir+"sun.png")))
    # set graph name, will show up in legend next to icon:
    customPlot.graph().setName("Data from Photovoltaic\nenergy barometer 2011")
    # set data:
    year =  [ 2005 , 2006 , 2007 , 2008  , 2009  , 2010 , 2011 ]
    value = [ 2.17 , 3.42 , 4.94 , 10.38 , 15.86 , 29.33 , 52.1 ]
    customPlot.graph().setData(year, value)


    font = QFont("sans", 12, QFont.Bold)
    text = QCPTextElement(customPlot, "Regenerative Energies", font)
    # set title of plot:
    customPlot.plotLayout().insertRow(0)
    customPlot.plotLayout().addElement(0, 0, text)
    # axis configurations:
    customPlot.xAxis.setLabel("Year")
    customPlot.yAxis.setLabel("Installed Gigawatts of\nphotovoltaic in the European Union")
    customPlot.xAxis2.setVisible(True)
    customPlot.yAxis2.setVisible(True)
    customPlot.xAxis2.setTickLabels(False)
    customPlot.yAxis2.setTickLabels(False)
    customPlot.xAxis2.setTicks(False)
    customPlot.yAxis2.setTicks(False)
    customPlot.xAxis2.setSubTicks(False)
    customPlot.yAxis2.setSubTicks(False)
    customPlot.xAxis.setRange(2004.5, 2011.5)
    customPlot.yAxis.setRange(0, 52)
    # setup legend:
    font2 = QFont(QtGui.QFont().family(), 7)
    customPlot.legend.setFont(font2)
    customPlot.legend.setIconSize(50, 20)
    customPlot.legend.setVisible(True)
    customPlot.axisRect().insetLayout().setInsetAlignment(0, Qt.AlignLeft | Qt.AlignTop)


    customPlot.rescaleAxes()

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




