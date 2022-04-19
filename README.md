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

### General
Installation of
- Qt 5.15.5 (e.g.MSVC 2017 Kit for Windows)
- libclang (version >= v8) libclang-release_80-based-windows-vs2017_64.7z (this is a higher version than on the pyside2 webpage) and including them into the environment variables
- CMake (>= 3.13) 

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
- MSVC 2019 Build Tools (Release) (from Viual Studio 2019 Installer)
  (Features: Windows Runtime, Core features, MSVC 142 VS 2019 C++ x64 build tools, Windows 10 SDK, C++ CMake tools, Build tools, Clang 142, C++ core features, VS SDK build core)
- OpenSSL: openssl-1.0.2j-fips-x86_64.zip
- Python >= 3.6 

* Environment settings
- set LLVM_INSTALL_DIR=c:\libclang
- set PATH=C:\Program Files\CMake\bin;e:\libclang\bin;E:\python\Python37;%PATH%
* Set QT path (adapt folder name)
- set Qt5_DIR=E:\Qt\5.15.5\msvc2017_64\lib\cmake\Qt5

* Create virtual environment
- python -m venv testenv 

* Build QCustomplot bindings
- CALL testenv\Scripts\activate.bat 

* Add build packages
- pip install cmake-build-extension wheel

* Build using python pip:
- python setup.py bdist_wheel

# We should use this, but there seems to be an issue still
# - pip wheel .  --no-deps -w wheelhouse/ 



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


