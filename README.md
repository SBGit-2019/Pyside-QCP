# Pyside2 bindings for QCustomplot

This project provides Python (v3.6 - v3.10) bindings for the popular OpenSource [QCustomPlot](https://www.qcustomplot.com/) (v2.01) Qt (v5.15.2) plotting library.
The bindings are provided for Linux and Windows (64bit).

The project can be found on [Github](https://github.com/SBGit-2019/Pyside-QCP/).

## Installation

You can install the library and run the examples with the following commands. Preferably you should do this in a python [*virtual environment*](https://docs.python.org/3/tutorial/venv.html).

    pip install qcustomplot
    qcustomplot_examples



## Examples
The folder [*qcustomplot_examples*](https://github.com/SBGit-2019/Pyside-QCP/tree/master/qcustomplot_examples) contains the examples from the QCustomplot C++ webpage translated to Python. 
These can be used as basis for own development or for seeing the features of the library. The example script *qcustomplot_examples* runs through all examples.

### Running all examples
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
    from qcustomplot import *

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


## License

This project is licensed under the GPL v3 License - see the [LICENSE](https://github.com/SBGit-2019/Pyside-QCP/blob/master/LICENSE) file for details.
Additionally, you can also use this project in commercial projects if you have a commercial license for the used libraries
- Qt 5.x
- QCustomPlot 2.x
The use of this python wheel is implicitly  also allowed when the above license requirements are fulfilled.

Note that commercial licenses are available for [QCustomPlot] at https://www.qcustomplot.com/.

## Acknowledgments

- Emanuel Eichhammer author of [QCustomPlot](https://www.qcustomplot.com/)
- [Qt] (https://www.qt.io/)




