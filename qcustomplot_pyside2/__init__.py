import sys
import os

__version__ = "0.15.2.1"
__version_info__ = (0, 15, 2.1, "", "")

# Add Pyside2 and shiboken2 to the search path
if sys.platform == 'win32':
    our_package_dir = os.path.abspath(os.path.dirname(__file__))
    dll_dir1 = os.path.normpath(os.path.join(our_package_dir, "../PySide2"))
    dll_dir2 = os.path.normpath(os.path.join(our_package_dir, "../shiboken2"))
    os.add_dll_directory(dll_dir1)
    os.add_dll_directory(dll_dir2)

# Only import after path is set
from .QCustomPlot import *



