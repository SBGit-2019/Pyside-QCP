# Pyside2 bindings for QCustomplot

This project creates Python (v3.x) bindings for the popular OpenSource [QCustomPlot](https://www.qcustomplot.com/) Qt (v5.x) plotting library.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Building instructions are provided for Linux and Windows 10.

### QCustomplot patches
Note, that the original QCustomplot 2.01 source code needs a handful of minor patches to compile with the current shiboken2 generator
(mainly due to bugs in the generator). Also the bindings generations on Windows 10 needs some minor adjustments. This project contains
a patchfile against the original [QCustomplot source code](https://www.qcustomplot.com/) and (probably temporarily) the original source files
(GPL V3) with the patch applied.

With these files a build can be made directly from this project.

### Prerequisites

The basic setup and the library and program sources are described on the following webpages. 
* Building [Pyside2 on Windows] (https://wiki.qt.io/Qt_for_Python/GettingStarted/Windows)
* Building [Pyside2 on Linux] (https://wiki.qt.io/Qt_for_Python/GettingStarted/X11)

Below is a detailled example installation process for Linux and Windows. At some points a bit newer library versions are used compared to the webpages (2019).
This will however be updated over time on the original pages. So check there as well.

A good example setup on how to build pyside2 bindings using [Shiboken](https://blog.basyskom.com/2019/using-shiboken2-to-create-python-bindings-for-a-qt-library/).

# Examples
In the folder *EXMAPLES* are the examples from the QCustomplot webpage translated to Python. 

### Running the examples
To run them the *PYTHONPATH* must point to the qcustomplot bindings libraries created or the python programs must be in the
same folder than the libraries. The shell scripts 'start.*' in the *EXAMPLES* folder set the path to these libararies
as created by the build process. For production environments you need to adapt the installation procedure of the libaries.

### Screenshots
See the [Wiki] (https://github.com/SBGit-2019/Pyside-QCP/wiki) for some screenshots.

## Building and Installation
### Installation for Ubuntu 18.04 or Mint 19:

Note: adapt the used paths to your own liking or needs
* Installation of build tools:
* System packages:
* We build pyside2 from source, so no need for: pip install PySide2
- apt install python3
- sudo apt-get  install llvm-6.0 virtualenvwrapper python3 python3-dev cmake build-essential git clang-6.0 libclang-6.0-dev libxslt-dev mesa-common-dev libgl1-mesa-glx libglib2.0-0 wget git libxkbcommon-x11-0 
- sudo apt-get  install libnss3 libasound2 libpulse-dev
     
* Install Cmake 3.13 and Qt 5.12.4:
* Download Qt from https://www.qt.io/
- cp DOWNLOAD_FOLDER/qt-opensource-linux-x64-5.12.4.run .
* Download CMake from https://cmake.org/download/ (adapt version number to your needs, minimum 3.13)
- cd /opt/extra
- wget https://github.com/Kitware/CMake/releases/download/v3.13.2/cmake-3.13.2-Linux-x86_64.tar.gz
- sudo tar xvf cmake-3.13.2-Linux-x86_64.tar.gz
- ./qt-opensource-linux-x64-5.12.4.run

* Set Paths (e.g. put in bashrc)
-  export LLVM_INSTALL_DIR=`llvm-config-6.0 --prefix`
-  export LD_LIBRARY_PATH=/opt/Qt5.12.4/5.12.4/gcc_64/lib
-  export PATH=/opt/Qt5.12.4/5.12.4/gcc_64/bin:$PATH
-  export Qt5_DIR=/opt/Qt5.12.4/5.12.4/gcc_64/lib/cmake/Qt5/
* To test type: 'qmake'

* Pyside virtual environment
* To create virtual environment
-  source /etc/bash_completion.d/virtualenvwrapper
-  mkvirtualenv -p `which python3` pyside2build

* To reactivate virtual environment
- source .virtualenvs/pyside2build/bin/activate

* Downloading and building pyside2
- mkdir pyside
-  cd pyside/
-  git clone --recursive https://code.qt.io/pyside/pyside-setup
-  cd pyside-setup && git checkout 5.12.4
-  git submodule update --init
* Building it
-  python setup.py install --qmake=/opt/Qt5.12.4/5.12.4/gcc_64/bin/qmake 
* Testing building of shiboken2 type: 'shiboken2'


### Installation for Windows 10:
(adapt the used paths to your own liking or needs)

**Note: For Windows all libraries MUST be created with the same or compatible MSVC versions (this includes, python, pyside2 and Qt)!!!
All build should be with the 'Release' version.**

* Installation of build tools:
- MSVC 2019 Build Tools (Release) [from Viual Studio 2019 Installer)
  (Features: Windows Runtime, Core features, MSVC 142 VS 2019 C++ x64 build tools, Windows 10 SDK, C++ CMake tools, Build tools, Clang 142, C++ core features, VS SDK build core)
- Qt 5.12.5 (MSVC 2017 Kit from qt-unified-windows-x86-3.1.1-online.exe)
- libclang (version >= v8) libclang-release_80-based-windows-vs2017_64.7z [this is a higher version than on the pyside2 webpage)
- OpenSSL: openssl-1.0.2j-fips-x86_64.zip
- CMake  (>= 3.13) 
- Python 3.7 (>= 3.8 is currently not supported by pyside2 build setup but will most likely work later)

* Environment settings
- set LLVM_INSTALL_DIR=c:\libclang
- segt PATH=C:\Program Files\CMake\bin;e:\libclang\bin;E:\python\Python37;%PATH%

* Create virtual environment
- python -m pip install virtualenv    
- python -m virtualenv testenv 
- pip install sphinx
* Some useful modules
- pip install  numpy PyOpenGL

* Building the pyside2 libraries:
- git clone --recursive https://code.qt.io/pyside/pyside-setup
- cd pyside-setup && git checkout 5.12
- python setup.py build --qmake=E:\Qt\5.12.0\msvc2015_64\bin\qmake.exe --openssl=C:\Dev\qtdev\OpenSSL-Win64\bin  --build-tests --ignore-git
- python setup.py install --qmake=E:\Qt\5.12.0\msvc2015_64\bin\qmake.exe  --openssl=C:\Dev\qtdev\OpenSSL-Win64\bin --build-tests --ignore-git
* Top Test pyside2: python examples/widgets/widgets/tetrix.py

* Build QCustomplot bindings
- Start visual studio X64 build shell (2019):
* Activate virtual environment
- CALL testenv\Scripts\activate.bat 
* Set QT path (adapt folder name)
- set Qt5_DIR=E:\Qt\5.12.5\msvc2017_64\lib\cmake\Qt5

* Build using cmake and nmake:
- cd BUILD
- cmake -H.. -B. -G "NMake Makefiles" -DCMAKE_BUILD_TYPE=Release
- nmake
- nmake install


## License

This project is licensed under the GPL v3 License - see the [LICENSE](https://github.com/SBGit-2019/Pyside-QCP/blob/master/LICENSE) file for details.
Note that commercial licenses are available for [QCustomPlot](https://www.qcustomplot.com/) if you want to use the library
not in an GPL V3 environment.

## Acknowledgments

* Emanuel Eichhammer author of [QCustomPlot](https://www.qcustomplot.com/)
* [Qt] (https://www.qt.io/)

