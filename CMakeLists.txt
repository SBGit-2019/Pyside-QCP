#****************************************************************************
#**                                                                        **
#**  QCustomPlot Pyside2 bindings are Python bindings for QCustomPlot/Qt   **
#**                                                                        **
#**                                                                        **
#**  This program is free software: you can redistribute it and/or modify  **
#**  it under the terms of the GNU General Public License as published by  **
#**  the Free Software Foundation, either version 3 of the License, or     **
#**  (at your option) any later version.                                   **
#**                                                                        **
#**  This program is distributed in the hope that it will be useful,       **
#**  but WITHOUT ANY WARRANTY; without even the implied warranty of        **
#**  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the         **
#**  GNU General Public License for more details.                          **
#**                                                                        **
#**  You should have received a copy of the GNU General Public License     **
#**  along with this program.  If not, see http://www.gnu.org/licenses/.   **
#**                                                                        **
#****************************************************************************
#**  Website/Contact: https://github.com/SBGit-2019/Pyside-QCP             **
#****************************************************************************

cmake_minimum_required(VERSION 3.13)
cmake_policy(VERSION 3.13)

# Enable policy to not use RPATH settings for install_name on macOS.
if(POLICY CMP0068)
  cmake_policy(SET CMP0068 NEW)
endif()


project(QCustomPlot-PySide2)

set(CMAKE_AUTOMOC ON)

# Find required Qt packages.
find_package(Qt5 5.12 REQUIRED COMPONENTS Core Gui Widgets PrintSupport)

set(CMAKE_CXX_STANDARD 11)
set(qcp_library "libqcustomplot")
set(bindings_library "QCustomPlot_PySide")
set(wrapped_header ${CMAKE_SOURCE_DIR}/bindings.h)
set(typesystem_file ${CMAKE_SOURCE_DIR}/bindings.xml)
set(generated_sources
  #  ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpabstractplottable1d_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcustomplot_pyside_module_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpitemline_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpcolorscale_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpcolorscaleaxisrectprivate_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpcolormapdata_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpaxis_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpgraph_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcustomplot_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpabstractplottable_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpabstractitem_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpfinancial_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpfinancialdatacontainer_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpfinancialdata_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpaxistickerdatetime_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpaxistickerlog_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpaxistickerpi_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpaxistickerfixed_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpaxistickertime_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpselectiondecoratorbracket_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpbarsgroup_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpitembracket_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpitempixmap_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpitemellipse_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpitemrect_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpitemcurve_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpitemstraightline_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcperrorbarsdata_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcperrorbars_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpcolormap_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpstatisticalboxdata_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpstatisticalbox_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpcurve_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpcurvedata_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcptextelement_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpcolorgradient_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcplegend_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpabstractlegenditem_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpselectionrect_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcplayout_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcplayoutinset_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcplayoutgrid_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpmargingroup_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpabstractpaintbuffer_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcppaintbufferpixmap_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcplayer_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpitemtext_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpitemanchor_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpitemposition_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpitemtracer_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpscatterstyle_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpgraphdata_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcp_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpdatarange_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpdataselection_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpplottableinterface1d_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpvector2d_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpaxispainterprivate_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpaxisticker_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpaxistickertext_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpbarsdata_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpbars_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpgrid_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcplineending_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcppainter_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpselectiondecorator_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcpaxisrect_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcplayerable_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcplayoutelement_wrapper.cpp
   ${CMAKE_CURRENT_BINARY_DIR}/${bindings_library}/qcprange_wrapper.cpp

   )

# ================================== Shiboken detection ======================================
# Use provided python interpreter if given.								   
find_package(Python3 REQUIRED COMPONENTS Interpreter Development)

if(NOT python_interpreter)
    find_program(python_interpreter "python")
endif()

set(PYSIDE2_DIR ${Python3_SITELIB}/PySide2)

if (WIN32)
    set(ld_prefix_var_name "PATH")
elseif(APPLE)
    set(ld_prefix_var_name "DYLD_LIBRARY_PATH")
else()
    set(ld_prefix_var_name "LD_LIBRARY_PATH")
endif()

# Macro to get various pyside / python include / link flags and paths.
# Uses the not entirely supported utils/pyside2_config.py file.				   
macro(pyside2_config option output_var)
    if(${ARGC} GREATER 2)
        set(is_list ${ARGV2})
    else()
        set(is_list "")
    endif()

    execute_process(
      COMMAND ${python_interpreter} "${CMAKE_SOURCE_DIR}/../utils/pyside2_config.py"
              ${option}
      OUTPUT_VARIABLE ${output_var}
      OUTPUT_STRIP_TRAILING_WHITESPACE)

    if ("${${output_var}}" STREQUAL "")
        message(FATAL_ERROR "Error: Calling pyside2_config.py ${option} returned no output.")
    endif()
    if(is_list)
        string (REPLACE " " ";" ${output_var} "${${output_var}}")
    endif()
endmacro()

pyside2_config(--shiboken2-module-path shiboken2_module_path)
pyside2_config(--shiboken2-generator-path shiboken2_generator_path)
pyside2_config(--python-include-path python_include_dir)
pyside2_config(--shiboken2-generator-include-path shiboken_include_dir 1)
pyside2_config(--shiboken2-module-shared-libraries-cmake shiboken_shared_libraries 0)
pyside2_config(--python-link-flags-cmake python_linking_data 0)
pyside2_config(--pyside2-path PYSIDE2_PATH)															   
#pyside2_config(--pyside2-shared-libraries-cmake PYSIDE2_SHARED_LIBRARIES 0)																	   
pyside2_config(--pyside2-shared-libraries-cmake pyside2_link 0)

set(shiboken_path "${shiboken2_generator_path}/shiboken2${CMAKE_EXECUTABLE_SUFFIX}")
if(NOT EXISTS ${shiboken_path})
    message(FATAL_ERROR "Shiboken executable not found at path: ${shiboken_path}")
endif()

# Get all relevant Qt include dirs, to pass them on to shiboken.
get_property(QT_CORE_INCLUDE_DIRS TARGET Qt5::Core PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
get_property(QT_GUI_INCLUDE_DIRS TARGET Qt5::Gui PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
get_property(QT_WIDGETS_INCLUDE_DIRS TARGET Qt5::Widgets PROPERTY INTERFACE_INCLUDE_DIRECTORIES)
set(QT_INCLUDE_DIRS ${QT_CORE_INCLUDE_DIRS} ${QT_GUI_INCLUDE_DIRS} ${QT_WIDGETS_INCLUDE_DIRS})
set(INCLUDES "")
foreach(INCLUDE_DIR ${QT_INCLUDE_DIRS})
    list(APPEND INCLUDES "-I${INCLUDE_DIR}")
endforeach()

# On macOS, check if Qt is a framework build. This affects how include paths should be handled.
get_target_property(QtCore_is_framework Qt5::Core FRAMEWORK)
if (QtCore_is_framework)
    get_target_property(qt_core_library_location Qt5::Core LOCATION)
    get_filename_component(qt_core_library_location_dir "${qt_core_library_location}" DIRECTORY)
    get_filename_component(lib_dir "${qt_core_library_location_dir}/../" ABSOLUTE)
    list(APPEND INCLUDES "--framework-include-paths=${lib_dir}")
endif()

# ==================================== RPATH configuration ====================================

# =============================================================================================
# !!! (The section below is deployment related, so in a real world application you will want to
# take care of this properly with some custom script or tool).
# =============================================================================================
# Enable rpaths so that the built shared libraries find their dependencies.
set(CMAKE_SKIP_BUILD_RPATH FALSE)
set(CMAKE_BUILD_WITH_INSTALL_RPATH TRUE)
set(CMAKE_INSTALL_RPATH ${shiboken2_module_path} ${CMAKE_CURRENT_SOURCE_DIR})
set(CMAKE_INSTALL_RPATH_USE_LINK_PATH TRUE)
# =============================================================================================
# !!! End of dubious section.
# =============================================================================================

# =============================== CMake target - qcp_library ===============================
# Define the sample shared library for which we will create bindings.
set(${qcp_library}_sources qcustomplot.cpp)
add_library(${qcp_library} SHARED ${${qcp_library}_sources})
target_link_libraries(${qcp_library} Qt5::Core Qt5::Widgets Qt5::Gui Qt5::PrintSupport)
set_property(TARGET ${qcp_library} PROPERTY PREFIX "")

get_target_property(qtcore_lib_includes Qt5::Core INTERFACE_INCLUDE_DIRECTORIES)
get_target_property(qtcore_lib_includes2 Qt5::Widgets INTERFACE_INCLUDE_DIRECTORIES)
get_target_property(qtcore_lib_includes3 Qt5::Gui INTERFACE_INCLUDE_DIRECTORIES)
get_target_property(qtcore_lib_includes4 Qt5::PrintSupport INTERFACE_INCLUDE_DIRECTORIES)
list(JOIN qtcore_lib_includes  ";-I" lib_includes)
set(lib_includes "-I${lib_includes}")


# Needed mostly on Windows to export symbols, and create a .lib file, otherwise the binding
# library can't link to the sample library.
target_compile_definitions(${qcp_library} PRIVATE QCUSTOMPLOT_COMPILE_LIBRARY)
target_compile_definitions(${qcp_library} INTERFACE QCUSTOMPLOT_USE_LIBRARY)

# ====================== Shiboken target for generating binding C++ files  ====================
# Set up the options to pass to shiboken.
set(shiboken_options --generator-set=shiboken --enable-parent-ctor-heuristic
    --enable-return-value-heuristic --use-isnull-as-nb_nonzero
    --avoid-protected-hack
    --enable-pyside-extensions
    ${lib_includes}
    -I${CMAKE_SOURCE_DIR}
    -T${CMAKE_SOURCE_DIR}
    -T${PYSIDE2_DIR}/typesystems/
    --output-directory=${CMAKE_CURRENT_BINARY_DIR}
    )

set(generated_sources_dependencies ${wrapped_header} ${typesystem_file})

# Add custom target to run shiboken to generate the binding cpp files.
add_custom_command(OUTPUT ${generated_sources}
                    COMMAND ${shiboken_path}
                    ${shiboken_options} ${wrapped_header} ${typesystem_file}
                    DEPENDS ${generated_sources_dependencies}
                    IMPLICIT_DEPENDS CXX ${wrapped_header}
                    WORKING_DIRECTORY ${CMAKE_CURRENT_BINARY_DIR}
                    COMMENT "Running generator for ${typesystem_file}.")

# =============================== CMake target - bindings_library =============================
# Set the cpp files which will be used for the bindings library.
set(${bindings_library}_sources ${generated_sources})

add_library(${bindings_library} MODULE ${${bindings_library}_sources})

# Apply relevant include and link flags.
target_include_directories(${bindings_library} PRIVATE ${python_include_dir})
target_include_directories(${bindings_library} PRIVATE ${PYSIDE2_DIR}/include/)
target_include_directories(${bindings_library} PRIVATE ${PYSIDE2_DIR}/include/QtCore)
target_include_directories(${bindings_library} PRIVATE ${PYSIDE2_DIR}/include/QtWidgets)
target_include_directories(${bindings_library} PRIVATE ${PYSIDE2_DIR}/include/QtGui)
target_include_directories(${bindings_library} PRIVATE ${PYSIDE2_DIR}/include/QtPrintSupport)
target_include_directories(${bindings_library} PRIVATE ${shiboken_include_dir})
target_include_directories(${bindings_library} PRIVATE ${CMAKE_SOURCE_DIR})

target_link_libraries(${bindings_library} PRIVATE ${shiboken_shared_libraries})
target_link_libraries(${bindings_library} PRIVATE ${qcp_library})
target_link_libraries(${bindings_library} PRIVATE ${pyside2_link})

# Adjust the name of generated module.
set_property(TARGET ${bindings_library} PROPERTY PREFIX "")
set_property(TARGET ${bindings_library} PROPERTY OUTPUT_NAME
             "${bindings_library}${PYTHON_EXTENSION_SUFFIX}")
	
if(WIN32)
    set_property(TARGET ${bindings_library} PROPERTY SUFFIX ".pyd")
endif()

# Make sure the linker doesn't complain about not finding Python symbols on macOS.
if(APPLE)
  set_target_properties(${bindings_library} PROPERTIES LINK_FLAGS "-undefined dynamic_lookup")
endif(APPLE)

# Find and link to the python import library only on Windows.
# On Linux and macOS, the undefined symbols will get resolved by the dynamic linker
# (the symbols will be picked up in the Python executable).
if (WIN32)
    list(GET python_linking_data 0 python_libdir)
    list(GET python_linking_data 1 python_lib)
    find_library(python_link_flags ${python_lib} PATHS ${python_libdir} HINTS ${python_libdir})
    target_link_libraries(${bindings_library} PRIVATE ${python_link_flags})
endif()


# ================================= Dubious deployment section ================================
if(WIN32)
    # =========================================================================================
    # !!! (The section below is deployment related, so in a real world application you will
    # want to take care of this properly (this is simply to eliminate errors that users usually
    # encounter.
    # =========================================================================================
    # Circumvent some "#pragma comment(lib)"s in "include/pyconfig.h" which might force to link
    # against a wrong python shared library.

    set(python_versions_list 3 32 33 34 35 36 37 38)
    set(python_additional_link_flags "")
    foreach(ver ${python_versions_list})
        set(python_additional_link_flags
            "${python_additional_link_flags} /NODEFAULTLIB:\"python${ver}_d.lib\"")
        set(python_additional_link_flags
            "${python_additional_link_flags} /NODEFAULTLIB:\"python${ver}.lib\"")
    endforeach()

    set_target_properties(${bindings_library}
                           PROPERTIES LINK_FLAGS "${python_additional_link_flags}")

    # Add custom target to hard-link shiboken shared libraries into the build folder, so that
    # the user doesn't have to set the PATH manually to point to the PySide2 package.
    foreach(library_path ${shiboken_shared_libraries})
        string(REGEX REPLACE ".lib$" ".dll" library_path ${library_path})
        get_filename_component(base_name ${library_path} NAME)
        file(TO_NATIVE_PATH ${library_path} source_path)
        file(TO_NATIVE_PATH "${CMAKE_CURRENT_BINARY_DIR}/${base_name}" dest_path)
        add_custom_command(OUTPUT "${base_name}"
                            COMMAND mklink /H "${dest_path}" "${source_path}"
                            DEPENDS ${library_path}
                            WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                            COMMENT "Creating hardlink to shiboken shared library ${base_name}")

        # Fake target that depends on the previous one, but has special ALL keyword, which means
        # it will always be executed.
        add_custom_target("fake_${base_name}" ALL DEPENDS ${base_name})
    endforeach()
    # =========================================================================================
    # !!! End of dubious section.
    # =========================================================================================
endif()

# =============================================================================================
# !!! (The section below is deployment related, so in a real world application you will want to
# take care of this properly with some custom script or tool).
# =============================================================================================
# Install the library and the bindings module into the source folder near the main.py file, so
# that the Python interpeter successfully imports the used module.
install(TARGETS ${bindings_library} ${qcp_library}
        LIBRARY DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}
        RUNTIME DESTINATION ${CMAKE_CURRENT_SOURCE_DIR}
        )
# =============================================================================================
# !!! End of dubious section.
# =============================================================================================



