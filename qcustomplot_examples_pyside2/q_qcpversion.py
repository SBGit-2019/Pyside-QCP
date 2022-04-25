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

import PySide2
import qcustomplot_pyside2
from qcustomplot_pyside2 import *

if __name__ == '__main__':
    print("QCustomPlot Bindings ",qcustomplot_pyside2.__version__)
    print("QCustomPlot Bindings ",qcustomplot_pyside2.__version_info__)
    print("QCustomPlot Version ",qcp_version())
    print("Pyside2 ",PySide2.__version__)
    print("Pyside2 ",PySide2.__version_info__)
    print("QtCore ",PySide2.QtCore.__version__)
    print("QtCore ",PySide2.QtCore.__version_info__)




