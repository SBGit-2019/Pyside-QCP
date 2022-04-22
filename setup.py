import setuptools
from setuptools import Extension
from setuptools.command.build_ext import build_ext
from subprocess import check_call, check_output, Popen, PIPE
import os
import sys
import platform
import pathlib
import subprocess
try:
    from configparser import ConfigParser
except ImportError:
    from ConfigParser import ConfigParser  # ver. < 3.0


# Write config
config = ConfigParser()
config.read('setup.cfg')
cpver = os.environ["MANYLINUX_PYTHON_VERSION"].replace(".","")
config.set('bdist_wheel', 'py_limited_api', "cp{}".format(cpver))
with open('setup.cfg', 'w') as configfile:
    config.write(configfile)


with open("README.md", "r") as fh:
    long_description = fh.read()

class CMakeExtension(Extension):
    def __init__(self, name, sourcedir, config=[]):
        Extension.__init__(self, name, sources=[], py_limited_api=True)
        self.sourcedir = os.path.abspath(sourcedir)
        self.config = config

class CMakeBuild(build_ext):
    def build_extensions(self):
        try:
            subprocess.check_output(["cmake", "--version"])
        except OSError:
            raise RuntimeError(
                "CMake must be installed to build the extensions: %s"
                % ", ".join(ext.name for ext in self.extensions)
            )
        cfg = "Debug" if self.debug else "Release"
        for ext in self.extensions:
            if not os.path.exists(self.build_temp):
                os.makedirs(self.build_temp)

            extdir = os.path.abspath(os.path.dirname(self.get_ext_fullpath(ext.name)))

            cmake_config_args = [
                "-DCMAKE_BUILD_TYPE={}".format(cfg),
                "-DMANYLINUX_PYTHON_VERSION={}".format(os.environ["MANYLINUX_PYTHON_VERSION"]),
                "-DCMAKE_LIBRARY_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir),
                "-DCMAKE_RUNTIME_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), extdir),
                "-DCMAKE_ARCHIVE_OUTPUT_DIRECTORY_{}={}".format(cfg.upper(), self.build_temp),
            ]

            make_location = os.path.abspath(self.build_temp)
            #print("MAKE LOC ",make_location)

            subprocess.check_call(
                ["cmake", ext.sourcedir] + cmake_config_args, cwd=make_location
            )
            print(ext.name)
            if platform.system() == "Windows":
              cdir = str(subprocess.check_output(["cd"], shell=True).decode()).strip()
              #subprocess.check_call(["dir"], shell=True)
            else:
              subprocess.check_call(["pwd"])
              print(extdir)
              subprocess.check_call(["ls"])

            lib_ext = ""
            lib_name = ""

            if platform.system() == "Darwin":
                lib_ext = ".dylib"
                lib_name = "libqcustomplot"
                thread_num = check_output(["sysctl", "-n", "hw.ncpu"], encoding="utf-8")
                subprocess.check_call(
                    ["make", "-C", make_location, "-j", str(thread_num).rstrip()], cwd=extdir
                )
            elif platform.system() == "Linux":
                lib_ext = ".so"
                lib_name = "libqcustomplot"
                thread_num = check_output(["nproc"], encoding="utf-8")
                print("MAKE_LOC ",make_location) # /io/Pyside-QCP/build/temp.linux-x86_64-cpython-38
                print("extdir ",extdir) #/io/Pyside-QCP/build/lib.linux-x86_64-cpython-38/qcustomplot
                subprocess.check_call(
                    ["make", "-C", make_location, "-j", str(thread_num).rstrip()], cwd=extdir
                )
                rpath="$ORIGIN/../PySide2:$ORIGIN/../PySide2/Qt/lib:$ORIGIN/../shiboken2"
                targetso = extdir+"/QCustomPlot.so"
                #subprocess.check_call(
                #   ["ls", "-l", targetso], shell=False)
                subprocess.check_call(
                   ["patchelf", "--remove-rpath", targetso], shell=False)
                subprocess.check_call(
                   ["patchelf", "--set-rpath", rpath, targetso], shell=False)
                print("Show new RPATH for ",targetso)
                subprocess.check_call(
                   ["patchelf", "--print-rpath", targetso], shell=False)
                #subprocess.check_call(
                #   ["ldd", targetso], shell=False)
            elif platform.system() == "Windows":
                lib_ext = ".pyd"
                lib_name = "qcustomplot"
                thread_num = 1
                # cmake --build . --target ALL_BUILD --config Release
                os.environ["PATH"] += os.pathsep + os.environ['VIRTUAL_ENV']+"/Lib/site-packages/shiboken2"
                subprocess.check_call(
                    ["cmake", "--build", ".", "--target", "ALL_BUILD", "--config",cfg], cwd=make_location
                , shell=True)


print("PACKAGES found (will be hardcoded to qcustomplot)=",setuptools.find_packages())
print("ENV ",os.environ["MANYLINUX_PYTHON_VERSION"])
print("CMAKE","-D MANYLINUX_PYTHON_VERSION={}".format(os.environ["MANYLINUX_PYTHON_VERSION"]))
#sys.exit()
setuptools.setup(
    name="qcustomplot",
    version="2.0.1",
    author="SBC",
    author_email="58021350+SBGit-2019@users.noreply.github.com",
    description="QCustomplot 2.0.1 for Pyside2 5.15.2",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SBGit-2019",
    keywords=["QCP", "QCustomPlot"],
    #packages=setuptools.find_packages(),
    packages=['qcustomplot', 'qcustomplot/qcp_examples'],
    package_data = {'qcustomplot': ['LICENSE*'], 'qcustomplot/qcp_examples':['*.py','*.ui', '*.jpg', '*.png']},
    
    
    #packages=[],
    ext_modules=[
        CMakeExtension("qcustomplot.libqcustomplot", ".", [])
    ],
    install_requires=[
        'PySide2==5.15.2.1',
        'shiboken2==5.15.2.1'
    ],
    python_requires='>=3.6',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Programming Language :: Python :: 3',
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: GPT3 License",
        "License :: OSI Approved :: Commercial",
        "Operating System :: Linux | Windows",
    ],
    include_package_data=True,
    cmdclass = {
        "build_ext": CMakeBuild
    },
)
