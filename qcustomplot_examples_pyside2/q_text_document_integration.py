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
from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout,QWidget,QMainWindow,QFileDialog
from PySide2.QtGui import QLinearGradient, QRadialGradient, QColor, QBrush, QPen, QFont, QPixmap, QPainterPath, QGuiApplication
from PySide2.QtCore import Qt, QMargins,QPointF,QObject,QCoreApplication,QFile,QTimer,QLocale,QDateTime,QDate,QSize,QTime,QSizeF,QMarginsF
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QTextFormat,QTextObjectInterface, QPicture,QTextCharFormat,QPyTextObject,QPageLayout,QPageSize
from PySide2.QtPrintSupport import QPrinter
from qcustomplot_pyside2 import *

class QCPDocumentObject(QPyTextObject):
    def __init__(self, parent):
      super(QCPDocumentObject,self).__init__(parent)

    def __del__(self):
      #print("DEL")
      pass

    def drawObject(self, painter, rect, doc, posInDocument, tformat):
      pic = tformat.property(MainWindow.QCPData)
      if pic==None:
          print("Plot is empty")
          return
      finalSize = pic.boundingRect().size()
      finalSize.scale(rect.size().toSize(), Qt.KeepAspectRatio)
      scaleFactor = float(finalSize.width())/float(pic.boundingRect().size().width())
      painter.save()
      painter.scale(scaleFactor, scaleFactor)
      painter.setClipRect(rect)
      painter.drawPicture(rect.topLeft(), pic)
      painter.restore()

    def intrinsicSize(self, doc, posInDocument, tformat):
      pic = tformat.property(MainWindow.QCPData)
      if pic==None:
          print("Plot is empty")
          return QSizeF(10,10)
      size = QSizeF(pic.boundingRect().size())
      return size;

    @staticmethod
    def generatePlotFormat(plot, width, height):
      picture = QPicture()
      qcpPainter = QCPPainter()
      qcpPainter.begin(picture)
      plot.toPainter(qcpPainter, width, height)
      qcpPainter.end()

      result = QTextCharFormat()
      result.setObjectType(MainWindow.QCPTextFormat)
      result.setProperty(MainWindow.QCPData, picture)
      return result

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
    QCPTextFormat = QtGui.QTextFormat.UserObject + 1
    QCPData = 1

    def __init__(self):
        super(MainWindow, self).__init__()

        our_package_dir = os.path.abspath(os.path.dirname(__file__))+"/"
        ui_file = QFile(our_package_dir+"text-document-integration.ui")
        ui_file.open(QFile.ReadOnly)
        loader = MyQUiLoader(self)
        loader.registerCustomWidget(QCustomPlot)
        self.ui = loader.load(ui_file)
        ui_file.close()

        self.ui.cbUseCurrentSize.toggled.connect(self.ui.sbWidth.setDisabled)
        self.ui.cbUseCurrentSize.toggled.connect(self.ui.sbHeight.setDisabled)

        self.ui.plot.axisRect().setMinimumSize(300, 180)
        self.setupPlot()
        plotObjectHandler = QCPDocumentObject(self)
        self.ui.textEdit.document().documentLayout().registerHandler(MainWindow.QCPTextFormat, plotObjectHandler)
        bla = self.textEdit.document().documentLayout().handlerForObject(MainWindow.QCPTextFormat)
        #print("Register handler ", bla)

        self.actionInsert_Plot.triggered.connect(self.on_actionInsert_Plot_triggered)
        self.actionSave_Document.triggered.connect(self.on_actionSave_Document_triggered)

    def on_actionInsert_Plot_triggered(self):
      #print("on_actionInsert_Plot_triggered")
      ui = self.ui
      cursor = ui.textEdit.textCursor()

      # insert the current plot at the cursor position. QCPDocumentObject::generatePlotFormat creates a
      # vectorized snapshot of the passed plot (with the specified width and height) which gets inserted
      # into the text document.
      if ui.cbUseCurrentSize.isChecked():
        width = 0
        height = 0
      else :
        width  = ui.sbWidth.value()
        height = ui.sbHeight.value()

      dd = QCPDocumentObject.generatePlotFormat(ui.plot, width, height)
      cursor.insertText(chr(0xfffc),dd)

      ui.textEdit.setTextCursor(cursor)

    def on_actionSave_Document_triggered(self):
      #print("on_actionSave_Document_triggered")
      ui = self.ui
      fileName = "./q_text-document-integration.pdf"
     #fileName = QFileDialog.getSaveFileName(self, "Save document...", qApp.applicationDirPath(), "*.pdf", None)
     #if fileName == None:
     #    print("No file")
     #    return
     #fileName = fileName[0]+".pdf"
      print("FILENAME=",fileName)

      printer = QPrinter()
      printer.setOutputFormat(QPrinter.PdfFormat)
      printer.setOutputFileName(fileName)
      pageMargins = QMargins(20, 20, 20, 20)
      pageLayout = QPageLayout()
      pageLayout.setMode(QPageLayout.StandardMode)
      pageLayout.setOrientation(QPageLayout.Portrait)
      pageLayout.setPageSize(QPageSize(QPageSize.A4))
      pageLayout.setUnits(QPageLayout.Millimeter)
      pageLayout.setMargins(QMarginsF(pageMargins))
      printer.setPageLayout(pageLayout);
      ui.textEdit.document().setPageSize(printer.pageRect().size())
      ui.textEdit.document().print_(printer)

    def setupPlot(self):
      # The following plot setup is mostly taken from the plot demos:
      ui = self.ui
      ui.plot.addGraph()
      ui.plot.graph(0).setPen(QPen(Qt.blue)) # line color blue for first graph
      ui.plot.graph(0).setBrush(QBrush(QColor(0, 0, 255, 20))) # first graph will be filled with translucent blue
      ui.plot.addGraph()
      ui.plot.graph(1).setPen(QPen(Qt.red)) # line color red for second graph
      # generate some points of data (y0 for first, y1 for second graph):
      x  = [0.0] * 250
      y0 = [0.0] * 250
      y1 = [0.0] * 250
      for i in range(0,250):
        x[i] = i
        y0[i] = math.exp(-i/150.0)*math.cos(i/10.0) # exponentially decaying cosine
        y1[i] = math.exp(-i/150.0) # exponential envelope

      # configure right and top axis to show ticks but no labels:
      # (see QCPAxisRect::setupFullAxesBox for a quicker method to do this)
      ui.plot.xAxis2.setVisible(True)
      ui.plot.xAxis2.setTickLabels(False)
      ui.plot.yAxis2.setVisible(True)
      ui.plot.yAxis2.setTickLabels(False)
      # make left and bottom axes always transfer their ranges to right and top axes:
      ui.plot.xAxis.rangeChanged.connect(ui.plot.xAxis2.setRange)
      ui.plot.yAxis.rangeChanged.connect(ui.plot.yAxis2.setRange)
      # pass data points to graphs:
      ui.plot.graph(0).setData(x, y0)
      ui.plot.graph(1).setData(x, y1)
      # let the ranges scale themselves so graph 0 fits perfectly in the visible area:
      ui.plot.graph(0).rescaleAxes()
      # same thing for graph 1, but only enlarge ranges (in case graph 1 is smaller than graph 0):
      ui.plot.graph(1).rescaleAxes(True)
      # Note: we could have also just called customPlot->rescaleAxes(); instead
      # Allow user to drag axis ranges with mouse, zoom with mouse wheel and select graphs by clicking:
      ui.plot.setInteractions(QCP.iRangeDrag | QCP.iRangeZoom | QCP.iSelectPlottables)

def demo(app, demotime=0):
    mainWin = MainWindow()
    screen = QGuiApplication.primaryScreen().geometry()
    mainWin.resize(screen.height(), screen.height()*0.75)	
    closeTimer = QTimer()
    closeTimer.timeout.connect(mainWin.close)
    if demotime > 0:
        closeTimer.start(demotime)
    mainWin.show()


    # Create and show the form
    # Run the main Qt loop
    res = app.exec_()
    mainWin.ui.plot = None
    return res


if __name__ == '__main__':
    # Create the Qt Application
    app = QApplication(sys.argv)
    res = demo(app)
    sys.exit(res)
