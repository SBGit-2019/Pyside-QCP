# Pyside2 bindings for QCustomplot

This project provides Python (v3.6 - v3.10) bindings for the popular OpenSource [QCustomPlot](https://www.qcustomplot.com/) (v2.1.0) Qt (v5.15.2) plotting library.
The bindings are provided for Linux and Windows (64bit).

The project can be found on [Github](https://github.com/SBGit-2019/Pyside-QCP/).

## Installation

You can install the library and run the examples with the following commands.
Preferably you should do this in a python [*virtual environment*](https://docs.python.org/3/tutorial/venv.html).

    pip install qcustomplot_pyside2  # Install latest version of the library
    qcustomplot_examples             # Start demos with default delay
    qcustomplot_examples 0           # Start demos without automatic continuation
    qcustomplot_examples 5000        # Continue demos every 5000 ms



## Examples
The folder [*qcustomplot_examples_pyside2*](https://github.com/SBGit-2019/Pyside-QCP/tree/master/qcustomplot_examples_pyside2) contains the examples from the QCustomplot C++ webpage translated to Python. 
These can be used as basis for own development or for seeing the features of the library. 

### Running all examples
The example command *qcustomplot_examples* linking to the script *all_demos.py* runs through all examples
with a default or user specified delay time.

- Install the matching python wheel from the wheels directory (preferably in a virtual environment).
- Start the shell script 'qcustomplot_examples' which will run all examples 


### Simple example code

    import shiboken2 as Shiboken
    from PySide2 import QtGui
    import sys
    import math
    from random import uniform,randint
    from PySide2.QtWidgets import QApplication, QDialog, QLineEdit, QPushButton, QVBoxLayout,QWidget,QMainWindow
    from PySide2.QtGui import QLinearGradient, QRadialGradient, QColor, QBrush, QPen, QFont, QPixmap, QPainterPath
    from PySide2.QtCore import Qt, QMargins,QPointF,QObject,QCoreApplication,QFile,QTimer,QLocale,QDateTime,QDate,QSize,QTime
    from PySide2.QtUiTools import QUiLoader
    from qcustomplot_pyside2 import *

    def demo(app):
      # Create plot
      customPlot = QCustomPlot()
      customPlot.resize(800, 600)
      customPlot.setWindowTitle('Quadratic Demo')

      # generate some data:
      x = [0.0] * 101 # initialize with entries 0..100
      y = [0.0] * 101 
      for i in range(0, 101):
        x[i] = i/50.0 - 1 # x goes from -1 to 1
        y[i] = x[i]*x[i]  # let's plot a quadratic function
    
      # create graph and assign data to it:
      customPlot.addGraph()
      customPlot.graph(0).setData(x, y)
      # give the axes some labels:
      customPlot.xAxis.setLabel("x")
      customPlot.yAxis.setLabel("y")
      # set axes ranges, so we see all data:
      customPlot.xAxis.setRange(-1, 1)
      customPlot.yAxis.setRange(0, 1)

      # show the plot
      customPlot.show()
      # run the main Qt loop
      res = app.exec_()
      # Make sure and manually reset pointer
      customPlot = None
      return res
   

    if __name__ == '__main__':
      # Create the Qt Application
      app = QApplication(sys.argv)
      res = demo(app)
      sys.exit(res)


## Screenshots
See the [Wiki] (https://github.com/SBGit-2019/Pyside-QCP/wiki) for some screenshots and explanations.
All screenshots can also be found in the [figures directory](https://github.com/SBGit-2019/Pyside-QCP/tree/master/FIG).

## Versions
The version naming of the Python bindings is analogue to the naming of the QCustomPlot library.
- v2.0.1: QCustomPlot library 2.0.1: All basic features
- v2.1.0: QCustomPlot library 2.1.0: Experimental radial plots and more bindings.
- v2.1.1: Small bugfixes
- v2.1.2: Small bugfixes for Scatterplot with single points
- v2.1.4: Bugfix for zero line and issue #4
- v2.1.5: Allow python access to all public fields of QCP (issue #5) 
          (Note: Access to QCP *public fields* has changed from methods, e.g. w.start() to fields, e.g. w.start, methods are available still as w.get_start())

## License

This project is licensed under the GPLv3+ License - see the [LICENSE](https://github.com/SBGit-2019/Pyside-QCP/blob/master/LICENSE) file for details.

Additionally, you can also use these bindings / these python wheels in commercial projects:
- if you have a commercial license for QCustomPlot 2.x
- fullfill the Qt license requirements, which typically mean you are using only the LGPL features of Qt 5.x or have a commercial license of Qt 5.x (as the bindings link only dynamically to Qt)

Note that commercial licenses are available for [QCustomPlot] at https://www.qcustomplot.com/.

## Acknowledgments

- Emanuel Eichhammer author of [QCustomPlot](https://www.qcustomplot.com/)
- [Qt] (https://www.qt.io/)




