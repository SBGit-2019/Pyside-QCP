FROM quay.io/pypa/manylinux2014_x86_64
LABEL maintainer SBGit <sbc-dev@posteo.de>

RUN cd /opt && \
    yum install -y libxslt-1.1.28-6.el7.x86_64 wget p7zip && \
    source /opt/rh/devtoolset-10/enable && \
    ln -s /opt/rh/devtoolset-10 /opt/rh/devtoolset-4 && \
    wget -q https://download.qt.io/archive/qt/5.15/5.15.2/single/qt-everywhere-src-5.15.2.tar.xz && \
    wget -q https://download.qt.io/development_releases/prebuilt/libclang/libclang-release_100-based-linux-Rhel7.6-gcc5.3-x86_64.7z && \
    /usr/libexec/p7zip/7za x libclang-release_100-based-linux-Rhel7.6-gcc5.3-x86_64.7z && \
    rm -rf libclang-release_100-based-linux-Rhel7.6-gcc5.3-x86_64.7z && \
    export LLVM_INSTALL_DIR=/opt/libclang && \
    ls -l /opt && \
    tar xf qt-everywhere-src-5.15.2.tar.xz && \
    rm -rf  qt-everywhere-src-5.15.2.tar.xz && \
    cd qt-everywhere-src-5.15.2 && \
    ./configure -release -nomake tests -nomake examples -confirm-license -opensource -prefix /opt/Qt  && \
    gmake -j4 && \
    gmake install && \
    cd /opt && \
    rm -rf qt-everywhere-src-5.15.2 && \
    ls -l /opt && \
    cd /
    

WORKDIR /io
CMD ["/bin/bash", "-c", "/io/Pyside-QCP/build-wheels.sh"]
#ENTRYPOINT ["/bin/bash", "-c", "/io/Pyside-QCP/build-wheels.sh"]

