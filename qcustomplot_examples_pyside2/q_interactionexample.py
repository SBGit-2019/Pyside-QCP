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
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout,QWidget,QMainWindow, QInputDialog
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
            #print("QCustomplot create")
            return QCustomPlot(parent)
        if parent is None:
            return self.baseinstance
        else:
            widget = QUiLoader.createWidget(self, className, parent, name)
            # print("yyxWidget=",widget," == ",className)
            setattr(self.baseinstance, name, widget)
            return widget

class MainWindow(QMainWindow):
    def addRandomGraph(self):
        n = 50 # number of points in graph

        style   = {1:QCPGraph.lsLine, 2:QCPGraph.lsStepLeft, 3:QCPGraph.lsStepRight, 4:QCPGraph.lsStepCenter, 5:QCPGraph.lsImpulse }
        scatter = {1:QCPScatterStyle.ssCross, 2:QCPScatterStyle.ssPlus, 3:QCPScatterStyle.ssCircle, 4:QCPScatterStyle.ssSquare, 5:QCPScatterStyle.ssDiamond, 6:QCPScatterStyle.ssDiamond }

        xScale  = (uniform(0,1) + 0.5)*2
        yScale  = (uniform(0,1) + 0.5)*2
        xOffset = (uniform(0,1) - 0.5)*4
        yOffset = (uniform(0,1) - 0.5)*10
        r1 = (uniform(0,1) - 0.5)*2
        r2 = (uniform(0,1) - 0.5)*2
        r3 = (uniform(0,1) - 0.5)*2
        r4 = (uniform(0,1) - 0.5)*2
        x = [0.0] * n
        y = [0.0] * n
        for i in range(0, n):
          x[i] = (float(i)/float(n)-0.5)*10.0*xScale + xOffset
          y[i] = (math.sin(x[i]*r1*5.0)*math.sin(math.cos(x[i]*r2)*r4*3.0)+r3*math.cos(math.sin(x[i])*r4*2.0))*yScale + yOffset

        gx = self.ui.customPlot.addGraph()
        #print("GX=",gx," and ",self.ui.customPlot.graph())
        gx.setName("New graph "+str(self.ui.customPlot.graphCount()-1))
        gx.setData(x, y)
        gx.setLineStyle(style[randint(1,5)]);
        if randint(0,100) >50:
            st = QCPScatterStyle(scatter[randint(1,6)])
            gx.setScatterStyle(st)
        graphPen = QPen()
        graphPen.setColor(QColor(randint(0,245)+10, randint(0,245)+10, randint(0,245)+10));
        graphPen.setWidthF(uniform(0,1)*2.0+1)
        gx.setPen(graphPen)
        self.ui.customPlot.replot()


    def __init__(self):
        super(MainWindow, self).__init__()

        our_package_dir = os.path.abspath(os.path.dirname(__file__))+"/"
        ui_file = QFile(our_package_dir+"mainwindow.ui")
        ui_file.open(QFile.ReadOnly)

        loader = MyQUiLoader(self)
        loader.registerCustomWidget(QCustomPlot)
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.ui.customPlot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectAxes | QCP.iSelectLegend | QCP.iSelectPlottables)
        self.ui.customPlot.xAxis.setRange(-8, 8)
        self.ui.customPlot.yAxis.setRange(-5, 5)
        self.ui.customPlot.axisRect().setupFullAxesBox()

        #self.ui.customPlot.plotLayout().insertRow(0)
        font =  QFont("sans", 24, QFont.Bold)
        title = QCPTextElement(self.ui.customPlot, "Interaction Example", font)
        #self.ui.customPlot.plotLayout().addElement(0, 0, title)

        self.ui.customPlot.xAxis.setLabel("x Axis")
        self.ui.customPlot.yAxis.setLabel("y Axis")
        self.ui.customPlot.legend.setVisible(True)
        legendFont = QtGui.QFont()
        legendFont.setPointSize(10)
        self.ui.customPlot.legend.setFont(legendFont)
        self.ui.customPlot.legend.setSelectedFont(legendFont)
        self.ui.customPlot.legend.setSelectableParts(QCPLegend.spItems) # legend box shall not be selectable, only legend items


        self.addRandomGraph()
        self.addRandomGraph()
        self.addRandomGraph()
        self.addRandomGraph()
        self.ui.customPlot.rescaleAxes()


        self.createMenus()
        # make bottom and left axes transfer their ranges to top and right axes:
        self.ui.customPlot.xAxis.rangeChanged.connect(self.ui.customPlot.xAxis2.setRange)
        self.ui.customPlot.yAxis.rangeChanged.connect(self.ui.customPlot.yAxis2.setRange)
        # connect some interaction slots:
        self.ui.customPlot.axisDoubleClick.connect(self.axisLabelDoubleClick)
        # connect slot that ties some axis selections together (especially opposite axes):
        self.ui.customPlot.selectionChangedByUser.connect(self.selectionChanged)
        # connect slot that shows a message in the status bar when a graph is clicked:
        self.ui.customPlot.plottableClick.connect(self.graphClicked)

    def graphClicked(self, plottable, dataIndex, event):
        # since we know we only have QCPGraphs in the plot, we can immediately access interface1D()
        # usually it's better to first check whether interface1D() returns non-zero, and only then use it.
        plottable.setName("Changed # "+str(dataIndex))
        # ERROR VALUE
        pi1d = plottable.interface1D()
        dataValue = pi1d.dataMainValue(dataIndex)
        dataValue2 = plottable.dataMainValue(dataIndex)
        # print("Datavalue ",dataValue, dataValue2)
        message = "Clicked on graph "+str(plottable.name())+" at data point "+str(dataIndex)+" with value "+str(dataValue2)
        self.ui.statusBar.showMessage(message, 2500)

    def selectionChanged(self):
        """
        normally, axis base line, axis tick labels and axis labels are selectable separately, but we want
        the user only to be able to select the axis as a whole, so we tie the selected states of the tick labels
        and the axis base line together. However, the axis label shall be selectable individually.

        The selection state of the left and right axes shall be synchronized as well as the state of the
        bottom and top axes.

        Further, we want to synchronize the selection of the graphs with the selection state of the respective
        legend item belonging to that graph. So the user can select a graph by either clicking on the graph itself
        or on its legend item.
        """
        b1 = (self.customPlot.xAxis.selectedParts())
        b2 = (self.customPlot.xAxis2.selectedParts())
        c1 = (self.customPlot.yAxis.selectedParts())
        c2 = (self.customPlot.yAxis2.selectedParts())
        # make top and bottom axes be selected synchronously, and handle axis and tick labels as one selectable object:
        if (b1 & (QCPAxis.spAxis|QCPAxis.spTickLabels) ) or (b2 &  (QCPAxis.spAxis|QCPAxis.spTickLabels)  ) :
            self.customPlot.xAxis.setSelectedParts (QCPAxis.spAxis | QCPAxis.spTickLabels)
            self.customPlot.xAxis2.setSelectedParts(QCPAxis.spAxis | QCPAxis.spTickLabels)
        # make left and right axes be selected synchronously, and handle axis and tick labels as one selectable object:
        if (c1 & (QCPAxis.spAxis|QCPAxis.spTickLabels) ) or (c2 &  (QCPAxis.spAxis|QCPAxis.spTickLabels)  ) :
            self.customPlot.yAxis.setSelectedParts (QCPAxis.spAxis | QCPAxis.spTickLabels)
            self.customPlot.yAxis2.setSelectedParts(QCPAxis.spAxis | QCPAxis.spTickLabels)

    def axisLabelDoubleClick(self, axis, part):
        if part == QCPAxis.spAxisLabel :
            newLabel = QInputDialog.getText(self, "QCustomPlot example", "New axis label:", QLineEdit.Normal, axis.label());
            if newLabel[1] :
              axis.setLabel(newLabel[0]);
              self.ui.customPlot.replot();


    def createMenus(self):
        self.fileMenu = self.menuBar.addMenu("&File")
        self.fileMenu.addSeparator()

        self.menuBar.addSeparator()

        self.helpMenu = self.menuBar.addMenu("&Help")

    def createStatusBar(self):
        self.statusBar().showMessage("Ready")


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
    mainWin.ui.customPlot = None
    return res

if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    res = demo(app)
    sys.exit(res)
