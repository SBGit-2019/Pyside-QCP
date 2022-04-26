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

class AxisTag(QObject):
    def __init__(self, parentAxis):
      parentPlot = parentAxis.parentPlot()
      #print("PARENT ",parentPlot)
      super().__init__(parentAxis)
      self.mAxis = parentAxis

      self.mDummyTracer = QCPItemTracer(parentPlot)
      self.mDummyTracer.setVisible(False)
      self.mDummyTracer.position().setTypeX(QCPItemPosition.ptAxisRectRatio)
      self.mDummyTracer.position().setTypeY(QCPItemPosition.ptPlotCoords)
      self.mDummyTracer.position().setAxisRect(self.mAxis.axisRect())
      self.mDummyTracer.position().setCoords(1, 0)
      self.mDummyTracer.position().setAxes(None, self.mAxis)

      # the arrow end (head) is set to move along with the dummy tracer by setting it as its parent
      # anchor. Its coordinate system (setCoords) is thus pixels, and this is how the needed horizontal
      # offset for the tag of the second y axis is achieved. This horizontal offset gets dynamically
      # updated in AxisTag::updatePosition. the arrow "start" is simply set to have the "end" as parent
      # anchor. It is given a horizontal offset to the right, which results in a 15 pixel long arrow.
      spike = QCPLineEnding(QCPLineEnding.esSpikeArrow)
      self.mArrow = QCPItemLine(parentPlot)
      self.mArrow.setLayer("overlay")
      self.mArrow.setClipToAxisRect(False)
      self.mArrow.setHead(spike)
      self.mArrow.end().setParentAnchor(self.mDummyTracer.position())
      self.mArrow.start().setParentAnchor(self.mArrow.end())
      self.mArrow.start().setCoords(15, 0)

      # The text label is anchored at the arrow start (tail) and has its "position" aligned at the
      # left, and vertically centered to the text label box.
      self.mLabel = QCPItemText(parentPlot)
      self.mLabel.setLayer("overlay")
      self.mLabel.setClipToAxisRect(False)
      self.mLabel.setPadding(QMargins(3, 0, 3, 0))
      #self.mLabel.setBrush(QBrush(Qt.white))
      self.mLabel.setBrush(QBrush(QColor(128,128,128,40)))
      self.mLabel.setPen(QPen(Qt.blue))
      self.mLabel.setPositionAlignment(Qt.AlignLeft|Qt.AlignVCenter)
      self.mLabel.position().setParentAnchor(self.mArrow.start())

    def __del__(self):
      pass
      #self.delete()

    def updatePosition(self, value):
      # since both the arrow and the text label are chained to the dummy tracer (via anchor
      # parent-child relationships) it is sufficient to update the dummy tracer coordinates. The
      # Horizontal coordinate type was set to ptAxisRectRatio so to keep it aligned at the right side
      # of the axis rect, it is always kept at 1. The vertical coordinate type was set to
      # ptPlotCoordinates of the passed parent axis, so the vertical coordinate is set to the new
      # value.
      self.mDummyTracer.position().setCoords(1, value)

      # We want the arrow head to be at the same horizontal position as the axis backbone, even if
      # the axis has a certain offset from the axis rect border (like the added second y axis). Thus we
      # set the horizontal pixel position of the arrow end (head) to the axis offset (the pixel
      # distance to the axis rect border). This works because the parent anchor of the arrow end is
      # the dummy tracer, which, as described earlier, is tied to the right axis rect border.
      self.mArrow.end().setCoords(self.mAxis.offset(), 0)

    def setText(self, text):
      self.mLabel.setText(text)

    def setPen(self, pen):
      self.mArrow.setPen(pen)
      self.mLabel.setPen(pen)

    def delete(self):
      #print("DEL AxisTag")
      self.mAxis = None
      if self.mArrow != None:
        parentPlot = self.mArrow.parentPlot()
        ok = parentPlot.removeItem(self.mArrow)
        #print("Remote item mArrow=",ok)
        self.mArrow = None
      if self.mLabel != None:
        parentPlot = self.mLabel.parentPlot()
        ok = parentPlot.removeItem(self.mLabel)
        #print("Remote item mLabel=",ok)
        self.mLabel = None
      if self.mDummyTracer != None:
        parentPlot = self.mDummyTracer.parentPlot()
        ok = parentPlot.removeItem(self.mDummyTracer)
        #print("Remote item mDummyTracer=",ok)
        self.mDummyTracer = None


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
        ui_file = QFile(our_package_dir+"axis-tags.ui")
        ui_file.open(QFile.ReadOnly)
        loader = MyQUiLoader(self)
        loader.registerCustomWidget(QCustomPlot)
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.mPlot = QCustomPlot(self.ui)
        self.ui.setCentralWidget(self.mPlot)

        mPlot=self.mPlot

        # configure plot to have two right axes:
        mPlot.yAxis.setTickLabels(False)
        mPlot.yAxis2.setVisible(True)
        mPlot.axisRect().addAxis(QCPAxis.atRight)
        mPlot.axisRect().axis(QCPAxis.atRight, 0).setPadding(30) # add some padding to have space for tags
        mPlot.axisRect().axis(QCPAxis.atRight, 1).setPadding(30) # add some padding to have space for tags

        # create graphs:
        self.mGraph1 = mPlot.addGraph(mPlot.xAxis, mPlot.axisRect().axis(QCPAxis.atRight, 0))
        self.mGraph2 = mPlot.addGraph(mPlot.xAxis, mPlot.axisRect().axis(QCPAxis.atRight, 1))
        self.mGraph1.setPen(QPen(QColor(250, 120, 0)))
        self.mGraph2.setPen(QPen(QColor(0, 180, 60)))

        # create tags with newly introduced AxisTag class (see axistag.h/.cpp):
        self.mTag1 = AxisTag(self.mGraph1.valueAxis())
        self.mTag1.setPen(self.mGraph1.pen())
        self.mTag2 = AxisTag(self.mGraph2.valueAxis())
        self.mTag2.setPen(self.mGraph2.pen())

        self.dataTimer = QTimer()
        self.dataTimer.timeout.connect(self.timerSlot)
        self.dataTimer.start(40)

    def timerSlot(self):
      # calculate and add a new data point to each graph:
      self.mGraph1.addData(self.mGraph1.dataCount(), math.sin(self.mGraph1.dataCount()/50.0)+math.sin(self.mGraph1.dataCount()/50.0/0.3843)*0.25)
      self.mGraph2.addData(self.mGraph2.dataCount(), math.cos(self.mGraph2.dataCount()/50.0)+math.sin(self.mGraph2.dataCount()/50.0/0.4364)*0.15)

      # make key axis range scroll with the data:
      self.mPlot.xAxis.rescale()
      self.mGraph1.rescaleValueAxis(False, True)
      self.mGraph2.rescaleValueAxis(False, True)
      self.mPlot.xAxis.setRange(self.mPlot.xAxis.range().upper, 100, Qt.AlignRight)

      # update the vertical axis tag positions and texts to match the rightmost data point of the graphs:
      graph1Value = self.mGraph1.dataMainValue(self.mGraph1.dataCount()-1)
      graph2Value = self.mGraph2.dataMainValue(self.mGraph2.dataCount()-1)
      s1 = "{:2.2f}".format(graph1Value)
      s2 = "{:2.2f}".format(graph2Value)
      self.mTag1.updatePosition(graph1Value)
      self.mTag2.updatePosition(graph2Value)
      self.mTag1.setText(s1)
      self.mTag2.setText(s2)

      self.mPlot.replot();

    def __del__(self):
      del self.dataTimer
      #äself.mTag1.delete()
      #self.mTag2.delete()
      self.ui.mPlot = None

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
    mainWin = None
    return res


if __name__ == '__main__':
    # Create the Qt Application
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)
    res = demo(app)
    sys.exit(res)


