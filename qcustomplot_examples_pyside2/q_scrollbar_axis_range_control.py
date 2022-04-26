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

class MyQUiLoader(QUiLoader):
    def __init__(self, baseinstance):
        QUiLoader.__init__(self)
        self.baseinstance = baseinstance

    def createWidget(self, className, parent=None, name=""):
        if className == "QCustomPlot":
            return QCustomPlot(parent)
        if parent is None:
            return self.baseinstance
        else:
            widget = QUiLoader.createWidget(self, className, parent, name)
            setattr(self.baseinstance, name, widget)
            return widget

class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        our_package_dir = os.path.abspath(os.path.dirname(__file__))+"/"
        ui_file = QFile(our_package_dir+"scrollwindow.ui")
        ui_file.open(QFile.ReadOnly)
        loader = MyQUiLoader(self)
        loader.registerCustomWidget(QCustomPlot)
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.setupPlot()

        #self.ui.plot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectAxes | QCP.iSelectLegend | QCP.iSelectPlottables)
        # configure scroll bars:
        # Since scroll bars only support integer values, we'll set a high default range of -500..500 and
        # divide scroll bar position values by 100 to provide a scroll range -5..5 in floating point
        # axis coordinates. if you want to dynamically grow the range accessible with the scroll bar,
        # just increase the the minimum/maximum values of the scroll bars as needed.
        self.ui.horizontalScrollBar.setRange(-500, 500);
        self.ui.verticalScrollBar.setRange(-500, 500);

        # create connection between axes and scroll bars:
        self.ui.horizontalScrollBar.valueChanged.connect(self.horzScrollBarChanged)
        self.ui.verticalScrollBar.valueChanged.connect(self.vertScrollBarChanged)
        self.ui.plot.xAxis.rangeChanged.connect(self.xAxisChanged)
        self.ui.plot.yAxis.rangeChanged.connect(self.yAxisChanged)

        # initialize axis range (and scroll bar positions via signals we just connected):
        self.ui.plot.xAxis.setRange(0, 6,  Qt.AlignCenter)
        self.ui.plot.yAxis.setRange(0, 10, Qt.AlignCenter)

    def xAxisChanged(self, range):
      self.ui.horizontalScrollBar.setValue(round(range.center()*100.0)) # adjust position of scroll bar slider
      self.ui.horizontalScrollBar.setPageStep(round(range.size()*100.0)) # adjust size of scroll bar slider

    def yAxisChanged(self, range):
      self.ui.verticalScrollBar.setValue(round(-range.center()*100.0)) # adjust position of scroll bar slider
      self.ui.verticalScrollBar.setPageStep(round(range.size()*100.0)) # adjust size of scroll bar slider

    def horzScrollBarChanged(self, value):
      if (abs(self.ui.plot.xAxis.range().center()-value/100.0) > 0.01): # if user is dragging plot, we don't want to replot twice
        self.ui.plot.xAxis.setRange(value/100.0, self.ui.plot.xAxis.range().size(), Qt.AlignCenter)
        self.ui.plot.replot();

    def vertScrollBarChanged(self, value):
      if (abs(self.ui.plot.yAxis.range().center()+value/100.0) > 0.01): # if user is dragging plot, we don't want to replot twice
        self.ui.plot.yAxis.setRange(-value/100.0, self.ui.plot.yAxis.range().size(), Qt.AlignCenter)
        self.ui.plot.replot();

    def setupPlot(self):
      # The following plot setup is mostly taken from the plot demos:
      self.ui.plot.addGraph()
      self.ui.plot.graph().setPen(QPen(Qt.blue))
      self.ui.plot.graph().setBrush(QBrush(QColor(0, 0, 255, 20)))
      self.ui.plot.addGraph()
      self.ui.plot.graph().setPen(QPen(Qt.red))
      x = [0.0] * 500
      y0 = [0.0] * 500
      y1 = [0.0] * 500
      for i in range(0,500):
        x[i] = (i/499.0-0.5)*10
        y0[i] = math.exp(-x[i]*x[i]*0.25)*math.sin(x[i]*5)*5
        y1[i] = math.exp(-x[i]*x[i]*0.25)*5

      self.ui.plot.graph(0).setData(x, y0)
      self.ui.plot.graph(1).setData(x, y1)
      self.ui.plot.axisRect().setupFullAxesBox(True)
      self.ui.plot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom)


def demo(app, demotime=0):
    mainWin = MainWindow()
    screen = QGuiApplication.primaryScreen().geometry()
    mainWin.resize(screen.height(), screen.height()*0.75)
    closeTimer = QTimer()
    closeTimer.timeout.connect(mainWin.close)
    if demotime > 0:
        closeTimer.start(demotime)
    mainWin.show()
    res = app.exec_()
    mainWin.ui.plot = None
    return res


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    res = demo(app)
    sys.exit(res)



