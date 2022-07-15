#!/bin/bash

# docker run -i -t -v `pwd`:/io quay.io/pypa/manylinux2014_x86_64_Qt /bin/bash -c /io/Pyside-QCP/build-wheels.sh
# or
# docker run -i -t -v `pwd`:/io quay.io/pypa/manylinux2014_x86_64_Qt /bin/bash
# cd /io/Pyside-QCP/
# ./build-wheels.sh

#set -e -u -x
set -e 
set -a 

#export PLAT="manylinux_2_17_x86_64"
export PLAT="manylinux2014_x86_64"

# Project directory from GIT
QCPDIR=/io/Pyside-QCP
VENV=/tmp/venv/pyside2
CACHE=/tmp/pycache
VERSION=2.1.2

echo "VENV="${VENV}
echo "QCPDIR="${QCPDIR}
echo "CACHE="${CACHE}

cd ${QCPDIR}
echo "Deleting wheelhouse ..."
rm -rf ${QCPDIR}/wheelhouse
mkdir ${CACHE}


ORG_LD_LIBRARY_PATH=${LD_LIBRARY_PATH}
ORG_PATH=${PATH}
echo "LIB " ${ORG_LD_LIBRARY_PATH}
echo "PATH " ${ORG_PATH}

# Compile wheels
for PYBIN in /opt/python/*/bin; do
     if  [[ ${PYBIN} =~  pypy ]]
     then
       echo "Ignore "${PYBIN} 
       continue
     fi
     #if  [[ ${PYBIN} !=  *cp38* ]]
     #then
     #  echo "Ignore no cp38 "${PYBIN} 
     #  continue
     #fi
     echo "Processing python interpreted "${PYBIN}

     PYLIB=${PYBIN/bin/lib}
     PYVER=""
     [[ ${PYBIN} =~ cp310-cp310/bin$ ]] &&  PYVER="3.10"
     [[ ${PYBIN} =~ cp39-cp39/bin$ ]] &&  PYVER="3.9"
     [[ ${PYBIN} =~ cp38-cp38/bin$ ]] &&  PYVER="3.8"
     [[ ${PYBIN} =~ cp37-cp37m/bin$ ]] &&  PYVER="3.7"
     [[ ${PYBIN} =~ cp36-cp36m/bin$ ]] &&  PYVER="3.6"
     [[ ${PYBIN} =~ pp39-pypy39_pp73/bin$ ]] &&  PYVER="3.9"
     [[ ${PYBIN} =~ pp38-pypy38_pp73/bin$ ]] &&  PYVER="3.8"
     [[ ${PYBIN} =~ pp37-pypy37_pp73/bin$ ]] &&  PYVER="3.7"
     echo "PYBIN="${PYBIN} "VER "${PYVER} "LIB " ${PYLIB}

     [[ ${PYBIN} =~ cp310-cp310/bin$ ]] &&  PYCP="310"
     [[ ${PYBIN} =~ cp39-cp39/bin$ ]] &&  PYCP="39"
     [[ ${PYBIN} =~ cp38-cp38/bin$ ]] &&  PYCP="38"
     [[ ${PYBIN} =~ cp37-cp37m/bin$ ]] &&  PYCP="37"
     [[ ${PYBIN} =~ cp36-cp36m/bin$ ]] &&  PYCP="36"


     PYSIDELIB=${VENV}/lib/python${PYVER}/site-packages/PySide2/Qt/lib/
     #CMAKEPATH=/io/cmake-3.22.4-linux-x86_64/bin
     export LD_LIBRARY_PATH=${PYSIDELIB}:${PYLIB}${ORG_LD_LIBRARY_PATH:+:${ORG_LD_LIBRARY_PATH}}
     #export PATH=${CMAKEPATH}:${PYBIN}${ORG_PATH:+:${ORG_PATH}}
     export PATH=${PYBIN}${ORG_PATH:+:${ORG_PATH}}
     echo "  LIB " ${LD_LIBRARY_PATH}
     echo "  PATH " ${PATH}
     export Qt5_DIR=/opt/Qt/lib/cmake/
     export LLVM_INSTALL_DIR=/opt/libclang

     rm -rf ${VENV}/
     python3 --version
     python3 -m venv ${VENV}/
     source ${VENV}//bin/activate
     #which python
     pip install --cache-dir ${CACHE} --index-url=http://download.qt.io/official_releases/QtForPython/  --trusted-host download.qt.io  shiboken2 pyside2 shiboken2_generator
     pip install --cache-dir ${CACHE} cmake-build-extension  wheel
     pip install --cache-dir ${CACHE} setuptools -U
     echo cmake -D MANYLINUX_PYTHON_VERSION=${PYVER} ..
     export  MANYLINUX_PYTHON_VERSION="${PYVER}"
     #python3 setup.py bdist_wheel
     #pip wheel ${QCPDIR}/ --no-clean --no-deps -w wheelhouse_${PYVER}/ 
     pip wheel ${QCPDIR}  --no-deps -w wheelhouse/ 
     echo "Result dir after build wheel:"
     ls -l ${QCPDIR}/wheelhouse


     #      qcustomplot_pyside2-2.0.1-cp38-abi3-linux_x86_64.whl
     #      qcustomplot_pyside2-2.0.1-cp310-abi3-linux_x86_64.whl
     wheel="qcustomplot_pyside2-${VERSION}-cp${PYCP}-abi3-linux_x86_64.whl"
     targetwheel="qcustomplot_pyside2-${VERSION}-cp${PYCP}-abi3-${PLAT}.whl"
     if [ -f "${QCPDIR}/wheelhouse/$targetwheel" ]; then
       rm -f ${QCPDIR}/wheelhouse/$targetwheel
     fi
     mv ${QCPDIR}/wheelhouse/$wheel ${QCPDIR}/wheelhouse/$targetwheel
     chmod a+r ${QCPDIR}/wheelhouse/$targetwheel
     echo "Result dir after move:"
     ls -l ${QCPDIR}/wheelhouse

     deactivate
     ls -l wheelhouse
     echo "-------------------------------------------------------------------------------------"
done
chmod a+rwx ${QCPDIR}/wheelhouse/

rm -rf ${VENV}/
rm -rf ${QCPDIR}/qcustomplot_pyside2.egg-info

echo "Ready."
