# Pyside2 bindings for QCustomplot

This project creates Python (v3.6-3.10) bindings for the popular OpenSource [QCustomPlot](https://www.qcustomplot.com/) (v2.01) Qt (v5.15.2) plotting library.

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
* Install the matching python wheel from the wheels directory (preferably in a virtual environment).
* Start the shell script 'start.*' in the *EXAMPLES* folder 

### Screenshots
See the [Wiki] (https://github.com/SBGit-2019/Pyside-QCP/wiki) for some screenshots.

## Building and Installation

### Linux
Building on Linux is done with a Dockerimage with a _manylinux2_ (manylinux_2_17_x86_64) distribution. 
The Dockerfile to create such an image is provided in the _Dockerfile_ or can be installed from 
Docker Hub as *lyxhub/manylinux2014_x86_64_qt*
Using
```
docker run -v /io:/io lyxhub/manylinux2014_x86_64_qt
```
This command will automatically create all Linux wheels in the directory _wheelhouse_.

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
Additionally, you can also use this project in commercial projects if you have a commercial license for the used libraries
* Qt 5.x
* QCustomPlot 2.x
The use of this python wheel is also allowed when the above license requirements are fullfilled.

Note that commercial licenses are available for [QCustomPlot] at https://www.qcustomplot.com/.

## Acknowledgments

* Emanuel Eichhammer author of [QCustomPlot](https://www.qcustomplot.com/)
* [Qt] (https://www.qt.io/)


