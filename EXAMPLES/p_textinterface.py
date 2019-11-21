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
from PySide2.QtGui import QLinearGradient, QRadialGradient, QColor, QBrush, QPen, QFont, QPixmap, QPainterPath
from PySide2.QtCore import Qt, QMargins,QPointF,QObject,QCoreApplication,QFile,QTimer,QLocale,QDateTime,QDate,QSize,QTime
from PySide2.QtUiTools import QUiLoader
from PySide2.QtSvg import QSvgRenderer
from PySide2.QtGui import QTextObjectInterface,QTextFormat,QTextCharFormat,QPyTextObject
from PySide2.QtCore import QSizeF,QByteArray
from PySide2.QtWidgets import  QMessageBox,QLabel,QLineEdit,QPushButton,QHBoxLayout,QVBoxLayout,QTextEdit
from QCustomPlot_PySide import *


class SvgTextObject(QPyTextObject):

    def __init__(self, parent):
        super(SvgTextObject,self).__init__(parent)

    def intrinsicSize(self, doc, posInDocument, tformat):
        a = tformat.property(Window.SvgData)
        b = QByteArray(a)
        renderer = QSvgRenderer(b)
        size = renderer.defaultSize()

        if size.height() > 25:
            size *= 25.0 / size.height()

        return QSizeF(size)

    def drawObject(self, painter, rect, doc, posInDocument, tformat):
        a = tformat.property(Window.SvgData)
        b = QByteArray(a)
        renderer = QSvgRenderer(b)
        renderer.render(painter, rect)


class Window(QWidget):

    SvgTextFormat = QtGui.QTextFormat.UserObject + 1

    SvgData = 1

    def __init__(self):
        super(Window, self).__init__()

        self.setupGui()
        self.setupTextObject()

        self.setWindowTitle(self.tr("Text Object Example"))

    def insertTextObject(self):
        fileName = self.fileNameLineEdit.text()
        file = QFile(fileName)

        if not file.open(QtCore.QIODevice.ReadOnly):
            QMessageBox.warning(self, self.tr("Error Opening File"),
                    self.tr("Could not open '%1'").arg(fileName))

        svgData = file.readAll()

        svgCharFormat = QTextCharFormat()
        svgCharFormat.setObjectType(Window.SvgTextFormat)
        svgCharFormat.setProperty(Window.SvgData, svgData)

        cursor = self.textEdit.textCursor()
        cursor.insertText("BLABLA")
        cursor.insertText(u"\uFFFC", svgCharFormat)
        #cursor.insertText(chr(0xfffc),svgCharFormat)
        cursor.insertText("BLABLA")
        self.textEdit.setTextCursor(cursor)

    def setupTextObject(self):
        svgInterface = SvgTextObject(self)
        self.textEdit.document().documentLayout().registerHandler(Window.SvgTextFormat, svgInterface)
        bla = self.textEdit.document().documentLayout().handlerForObject(Window.SvgTextFormat)
        print("Register handler ", svgInterface)
        print("Register handler search ", bla)
        self.bla = svgInterface

    def setupGui(self):
        fileNameLabel = QLabel(self.tr("Svg File Name:"))
        self.fileNameLineEdit = QLineEdit()
        insertTextObjectButton = QPushButton(self.tr("Insert Image"))

        self.fileNameLineEdit.setText('./heart.svg')
        QtCore.QObject.connect(insertTextObjectButton, QtCore.SIGNAL('clicked()'), self.insertTextObject)

        bottomLayout = QHBoxLayout()
        bottomLayout.addWidget(fileNameLabel)
        bottomLayout.addWidget(self.fileNameLineEdit)
        bottomLayout.addWidget(insertTextObjectButton)

        self.textEdit = QTextEdit()

        mainLayout = QVBoxLayout()
        mainLayout.addWidget(self.textEdit)
        mainLayout.addLayout(bottomLayout)

        self.setLayout(mainLayout)


if __name__ == '__main__':

    import sys

    app = QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())
