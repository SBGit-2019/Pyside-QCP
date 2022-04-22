# Building Pyside2 bindings for QCustomplot

This project creates Python (v3.6-3.10) bindings for the popular OpenSource [QCustomPlot](https://www.qcustomplot.com/) (v2.01) Qt (v5.15.2) plotting library.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
Building instructions are provided for Linux and Windows 10.

### QCustomplot patches
Note, that the original QCustomplot 2.x source code needs a handful of minor patches to compile with the current shiboken2 generator
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
In the folder *qcustomplot/qcp_examples* are the examples from the QCustomplot webpage translated to Python. 

### Running the examples
* Install the matching python wheel from the wheels directory (preferably in a virtual environment).
* Start the shell script 'start.*' in the *qcustomplot/qcp_examples* folder 

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

The github workflow _build_linux_wheels.yml_ performs this.

### Installation for Windows 10:
Installation of Qt and LLVM environment:
- Qt 5.15.5 (e.g. MSVC 2017 Kit for Windows)
- libclang (version >= v8) libclang-release_80-based-windows-vs2017_64.7z and including them into the environment variables
- CMake (>= 3.13) 


* Installation of build tools:

  - MSVC v142 VS 2019 Build Tools (Release) (from Viual Studio 2019 Installer)

  - Windows 10 SDK (10.0.18362.0)

- Optionally OpenSSL: openssl-1.0.2j-fips-x86_64.zip
- Python >= 3.6 

**Note**:

-  For Windows all libraries MUST be created with the same or compatible MSVC versions (this includes, python, pyside2 and Qt)
- All build should be with the 'Release' version.
- Very important, you *MUST NOT* install visual studio / build tools of a too recent version (tested and working is **16.3.8**). Using a too high version will introduce bad generator errors in the shiboken runs! Earlier versions can be downloaded from
  [Visual Studio](https://docs.microsoft.com/en-us/visualstudio/releases/2019/history#installing-an-earlier-release).
* Environment settings

  - set LLVM_INSTALL_DIR=e:\libclang

  - set Qt5_DIR=E:\Qt\5.15.5\msvc2017_64

* Create virtual environment
  - python -m venv testenv 

* Activate environment
  - CALL testenv\Scripts\activate.bat 

* Add build packages

  * pip install --index-url=http://download.qt.io/official_releases/QtForPython/  --trusted-host download.qt.io  shiboken2 pyside2 shiboken2_generator
  - pip install cmake-build-extension wheel setuptools-U

* Build using python pip:
  - pip wheel . --no-deps  -w wheelhouse/ # Preferred
  - (python setup.py bdist_wheel  # as Alternative for more debugging output)




The github workflow ``build_windows_wheels.yml``_ performs all this.
