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

lastFpsKey = 0.0
frameCount = 0

def bracketDataSlot():
  global frameCount
  global lastFpsKey
  global customPlot
  global itemDemoPhaseTracer

  secs = QCPAxisTickerDateTime.dateTimeToKey(QDateTime.currentDateTime())

  # update data to make phase move:
  n = 500
  phase = secs*5
  k = 3
  x = [0.0] * n
  y = [0.0] * n
  for i in range(0, n):
    x[i] = i/(n-1)*34 - 17
    y[i] = math.exp(-x[i]*x[i]/20.0)*math.sin(k*x[i]+phase)

  customPlot.graph().setData(x, y)

  itemDemoPhaseTracer.setGraphKey((8*math.pi+math.fmod(math.pi*1.5-phase, 6*math.pi))/k)

  customPlot.replot()

  # calculate frames per second:
  key = secs
  frameCount += 1

  if key-lastFpsKey > 2: # average fps over 2 seconds
      fps = float(frameCount)/(float)(key-lastFpsKey)
      fps_str = '{:3.2f}'.format(fps)
      customPlot.setWindowTitle('Real Time Data Demo FPS: '+fps_str)
      lastFpsKey = key
      frameCount = 0




def demo(app, demotime=0):
    global customPlot
    global itemDemoPhaseTracer
    customPlot = QCustomPlot()
    screen = QGuiApplication.primaryScreen().geometry()
    customPlot.resize(screen.height(), screen.height()*0.75)
    customPlot.setWindowTitle('Item Demo')

    customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom)
    graph = customPlot.addGraph()
    n = 500
    phase = 0
    k = 3
    x = [0.0] * n
    y = [0.0] * n
    for i in range(0, n):
      x[i] = i/(n-1)*34 - 17
      y[i] = math.exp(-x[i]*x[i]/20.0)*math.sin(k*x[i]+phase)

    xAxis = customPlot.yAxis
    gridX = xAxis.grid()
    graph.setData(x, y)
    graph.setPen(QPen(Qt.blue))
    graph.rescaleKeyAxis()
    customPlot.yAxis.setRange(-1.45, 1.65)
    gridX.setZeroLinePen(Qt.NoPen)

    # add the bracket at the top:
    bracket = QCPItemBracket(customPlot)
    bracket.left().setCoords(-8, 1.1)
    bracket.right().setCoords(8, 1.1)
    bracket.setLength(13)

    # add the text label at the top:
    wavePacketText = QCPItemText(customPlot)
    # ToDo: wavePacketText.position2().setParentAnchor(bracket.center)
    wavePacketText.position().setCoords(0, -10) # move 10 pixels to the top from bracket center anchor  # ToDo: position2?
    wavePacketText.setPositionAlignment(Qt.AlignBottom|Qt.AlignHCenter)
    wavePacketText.setText("Wavepacket")
    wavePacketText.setFont(QFont(QtGui.QFont().family(), 10))

    # add the phase tracer (red circle) which sticks to the graph data (and gets updated in bracketDataSlot by timer event):
    phaseTracer = QCPItemTracer(customPlot)
    itemDemoPhaseTracer = phaseTracer # so we can access it later in the bracketDataSlot for animation
    phaseTracer.setGraph(graph)
    phaseTracer.setGraphKey((math.pi*1.5-phase)/k)
    phaseTracer.setInterpolating(True)
    phaseTracer.setStyle(QCPItemTracer.tsCircle)
    phaseTracer.setPen(QPen(Qt.red))
    phaseTracer.setBrush(Qt.red)
    phaseTracer.setSize(7)

    # add label for phase tracer:
    phaseTracerText = QCPItemText(customPlot)
    phaseTracerText.position().setType(QCPItemPosition.ptAxisRectRatio)   # ToDo: position2?
    phaseTracerText.setPositionAlignment(Qt.AlignRight|Qt.AlignBottom)
    phaseTracerText.position().setCoords(1.0, 0.95) # lower right corner of axis rect   # ToDo: position2?
    phaseTracerText.setText("Points of fixed\nphase define\nphase velocity vp")
    phaseTracerText.setTextAlignment(Qt.AlignLeft)
    phaseTracerText.setFont(QFont(QtGui.QFont().family(), 9))
    phaseTracerText.setPadding(QMargins(8, 0, 0, 0))

    # add arrow pointing at phase tracer, coming from label:
    spike = QCPLineEnding(QCPLineEnding.esSpikeArrow)
    phaseTracerArrow = QCPItemCurve(customPlot)
    phaseTracerArrow.start().setParentAnchor(phaseTracerText.left())
    phaseTracerArrow.startDir().setParentAnchor(phaseTracerArrow.start())
    phaseTracerArrow.startDir().setCoords(-40, 0) # direction 30 pixels to the left of parent anchor (tracerArrow.start)
    phaseTracerArrow.end().setParentAnchor(phaseTracer.position())
    phaseTracerArrow.end().setCoords(10, 10)
    phaseTracerArrow.endDir().setParentAnchor(phaseTracerArrow.end())
    phaseTracerArrow.endDir().setCoords(30, 30)
    phaseTracerArrow.setHead(spike)
    phaseTracerArrow.setTail(QCPLineEnding(QCPLineEnding.esBar, (phaseTracerText.bottom().pixelPosition().y()-phaseTracerText.top().pixelPosition().y())*0.85))

    # add the group velocity tracer (green circle):
    groupTracer = QCPItemTracer(customPlot)
    groupTracer.setGraph(graph)
    groupTracer.setGraphKey(5.5)
    groupTracer.setInterpolating(True)
    groupTracer.setStyle(QCPItemTracer.tsCircle)
    groupTracer.setPen(QPen(Qt.green))
    groupTracer.setBrush(Qt.green)
    groupTracer.setSize(7)

    # add label for group tracer:
    groupTracerText = QCPItemText(customPlot)
    groupTracerText.position().setType(QCPItemPosition.ptAxisRectRatio)   # ToDo: position2?
    groupTracerText.setPositionAlignment(Qt.AlignRight|Qt.AlignTop)
    groupTracerText.position().setCoords(1.0, 0.20) # lower right corner of axis rect   # ToDo: position2?
    groupTracerText.setText("Fixed positions in\nwave packet define\ngroup velocity vg")
    groupTracerText.setTextAlignment(Qt.AlignLeft)
    groupTracerText.setFont(QFont(QtGui.QFont().family(), 9))
    groupTracerText.setPadding(QMargins(8, 0, 0, 0))

    # add arrow pointing at group tracer, coming from label:
    groupTracerArrow = QCPItemCurve(customPlot)
    groupTracerArrow.start().setParentAnchor(groupTracerText.left())
    groupTracerArrow.startDir().setParentAnchor(groupTracerArrow.start())
    groupTracerArrow.startDir().setCoords(-40, 0) # direction 30 pixels to the left of parent anchor (tracerArrow.start)
    groupTracerArrow.end().setCoords(5.5, 0.4)
    groupTracerArrow.endDir().setParentAnchor(groupTracerArrow.end())
    groupTracerArrow.endDir().setCoords(0, -40)
    groupTracerArrow.setHead(spike)
    groupTracerArrow.setTail(QCPLineEnding(QCPLineEnding.esBar, (groupTracerText.bottom().pixelPosition().y()-groupTracerText.top().pixelPosition().y())*0.85))

    # add dispersion arrow:
    arrow = QCPItemCurve(customPlot)
    arrow.start().setCoords(1, -1.1)
    arrow.startDir().setCoords(-1, -1.3)
    arrow.endDir().setCoords(-5, -0.3)
    arrow.end().setCoords(-10, -0.2)
    arrow.setHead(spike)

    # add the dispersion arrow label:
    dispersionText = QCPItemText(customPlot)
    dispersionText.position().setCoords(-6, -0.9)
    dispersionText.setRotation(40)
    dispersionText.setText("Dispersion with\nvp < vg")
    dispersionText.setFont(QFont(QtGui.QFont().family(), 10))

    # setup a timer that repeatedly calls MainWindow.bracketDataSlot:
    # ToDo: dataTimer.timeout.connect(this.bracketDataSlot)
    # ToDo: dataTimer.start(0) # Interval 0 means to refresh as fast as possible"""
    dataTimer = QTimer()
    dataTimer.timeout.connect(bracketDataSlot)
    dataTimer.start(0)

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



