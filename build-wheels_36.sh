#!/bin/bash

# Quit shell on error
set -e 
# Export all defined variables
set -a 

export PLAT="manylinux2014_x86_64"

# Project directory from GIT
export QCPDIR=/io/Pyside-QCP
export VENV=/tmp/venv/pyside2
export CACHE=/tmp/pycache
export VERSION=2.1.3

echo "VENV="${VENV}
echo "QCPDIR="${QCPDIR}
echo "CACHE="${CACHE}

cd ${QCPDIR}
echo "Deleting wheelhouse ..."
rm -rf ${QCPDIR}/wheelhouse
mkdir ${QCPDIR}/wheelhouse
mkdir ${CACHE}


export ORG_LD_LIBRARY_PATH=${LD_LIBRARY_PATH}
export ORG_PATH=${PATH}
echo "LIB " ${ORG_LD_LIBRARY_PATH}
echo "PATH " ${ORG_PATH}

export PYBIN=/opt/python/cp36-cp36m/bin
export PYLIB=${PYBIN/../lib}
export PYVER="3.6"

export PYSIDELIB=${VENV}/lib/python${PYVER}/site-packages/PySide2/Qt/lib/
export LD_LIBRARY_PATH=${PYSIDELIB}:${PYLIB}${ORG_LD_LIBRARY_PATH:+:${ORG_LD_LIBRARY_PATH}}
export PATH=${PYBIN}${ORG_PATH:+:${ORG_PATH}}
echo "  LIB " ${LD_LIBRARY_PATH}
echo "  PATH " ${PATH}
export Qt5_DIR=/opt/Qt/lib/cmake/
export LLVM_INSTALL_DIR=/opt/libclang

rm -rf ${VENV}/
python3 --version
python3 -m venv ${VENV}/
source ${VENV}//bin/activate

python -m pip install pip==21.2.1
pip install --cache-dir ${CACHE} cmake-build-extension==0.5.0 wheel==0.37.1
pip install --cache-dir ${CACHE} setuptools==59.6.0
pip install --cache-dir ${CACHE} --index-url=http://download.qt.io/official_releases/QtForPython/  --trusted-host download.qt.io  shiboken2==5.15.2.1  pyside2==5.15.2.1 shiboken2_generator==5.15.2.1
echo cmake -D MANYLINUX_PYTHON_VERSION=${PYVER} ..
export  MANYLINUX_PYTHON_VERSION="${PYVER}"
pip wheel ${QCPDIR}  --no-deps -w wheelhouse/ 
echo "Result dir after build wheel:"
ls -l ${QCPDIR}/wheelhouse


chmod a+rwx ${QCPDIR}/wheelhouse/

echo "Ready."
