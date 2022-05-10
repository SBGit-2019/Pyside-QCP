import sys
import os
import signal
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QCoreApplication

import qcustomplot_examples_pyside2.q_advancedaxesdemo
import qcustomplot_examples_pyside2.q_axistags
import qcustomplot_examples_pyside2.q_barchartdemo
import qcustomplot_examples_pyside2.q_colormapdemo
import qcustomplot_examples_pyside2.q_datedemo
import qcustomplot_examples_pyside2.q_financialdemo
import qcustomplot_examples_pyside2.q_interactionexample
import qcustomplot_examples_pyside2.q_itemdemo
import qcustomplot_examples_pyside2.q_linestyledemo
import qcustomplot_examples_pyside2.q_logarithmicdemo
import qcustomplot_examples_pyside2.q_multiaxisdemo
import qcustomplot_examples_pyside2.q_parametriccurvesdemo
import qcustomplot_examples_pyside2.q_quadraticdemo
import qcustomplot_examples_pyside2.q_realtimedatademo
import qcustomplot_examples_pyside2.q_scatterpixmapdemo
import qcustomplot_examples_pyside2.q_scatterstyledemo
import qcustomplot_examples_pyside2.q_scrollbar_axis_range_control
import qcustomplot_examples_pyside2.q_simpledemo
import qcustomplot_examples_pyside2.q_simpleitemdemo
import qcustomplot_examples_pyside2.q_sincscatterdemo
import qcustomplot_examples_pyside2.q_statisticaldemo
import qcustomplot_examples_pyside2.q_styleddemo
import qcustomplot_examples_pyside2.q_text_document_integration
import qcustomplot_examples_pyside2.q_textinterface
import qcustomplot_examples_pyside2.q_texturebrushdemo
import qcustomplot_examples_pyside2.q_polarplotdemo

def main(demotime=7500):
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    if sys.platform == 'win32':
        signal.signal(signal.SIGBREAK, signal.SIG_DFL)
    if len(sys.argv) > 1:
        demotime = int(sys.argv.pop(1))
    if demotime == 0:
        print(f"There is no automatic slide switching. Close the window to continue.")
    else:
        print(f"Automatic demo slide switching after {demotime} ms enabled.")


    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)

    print("q_advancedaxesdemo")
    qcustomplot_examples_pyside2.q_advancedaxesdemo.demo(app, demotime)
    print("q_axistags")
    qcustomplot_examples_pyside2.q_axistags.demo(app, demotime)
    print("q_barchartdemo")
    qcustomplot_examples_pyside2.q_barchartdemo.demo(app, demotime)
    print("q_colormapdemo")
    qcustomplot_examples_pyside2.q_colormapdemo.demo(app, demotime)
    print("q_datedemo")
    qcustomplot_examples_pyside2.q_datedemo.demo(app, demotime)
    print("q_financialdemo")
    qcustomplot_examples_pyside2.q_financialdemo.demo(app, demotime)
    print("q_itemdemo")
    qcustomplot_examples_pyside2.q_itemdemo.demo(app, demotime)
    print("q_interactionexample")
    qcustomplot_examples_pyside2.q_interactionexample.demo(app, demotime)
    print("q_linestyledemo")
    qcustomplot_examples_pyside2.q_linestyledemo.demo(app, demotime)
    print("q_logarithmicdemo")
    qcustomplot_examples_pyside2.q_logarithmicdemo.demo(app, demotime)
    print("q_multiaxisdemo")
    qcustomplot_examples_pyside2.q_multiaxisdemo.demo(app, demotime)
    print("q_parametriccurvesdemo")
    qcustomplot_examples_pyside2.q_parametriccurvesdemo.demo(app, demotime)
    print("q_quadraticdemo")
    qcustomplot_examples_pyside2.q_quadraticdemo.demo(app, demotime)
    print("q_realtimedatademo")
    qcustomplot_examples_pyside2.q_realtimedatademo.demo(app, demotime)
    print("q_scatterpixmapdemo")
    qcustomplot_examples_pyside2.q_scatterpixmapdemo.demo(app, demotime)
    print("q_scatterstyledemo")
    qcustomplot_examples_pyside2.q_scatterstyledemo.demo(app, demotime)
    print("q_scrollbar_axis_range_control")
    qcustomplot_examples_pyside2.q_scrollbar_axis_range_control.demo(app, demotime)
    print("q_simpledemo")
    qcustomplot_examples_pyside2.q_simpledemo.demo(app, demotime)
    print("q_simpleitemdemo")
    qcustomplot_examples_pyside2.q_simpleitemdemo.demo(app, demotime)
    print("q_sincscatterdemo")
    qcustomplot_examples_pyside2.q_sincscatterdemo.demo(app, demotime)
    print("q_statisticaldemo")
    qcustomplot_examples_pyside2.q_statisticaldemo.demo(app, demotime)
    print("q_styleddemo")
    qcustomplot_examples_pyside2.q_styleddemo.demo(app, demotime)
    print("q_text_document_integration")
    qcustomplot_examples_pyside2.q_text_document_integration.demo(app, demotime)
    print("q_textinterface")
    qcustomplot_examples_pyside2.q_textinterface.demo(app, demotime)
    print("q_texturebrushdemo")
    qcustomplot_examples_pyside2.q_texturebrushdemo.demo(app, demotime)
    print("q_polarplotdemo")
    qcustomplot_examples_pyside2.q_polarplotdemo.demo(app, demotime)


if __name__ == '__main__':
    if len(sys.argv) > 1:
        demotime = int(sys.argv[1])
    else:
        demotime = 7500
    main(demotime)
    sys.exit(0)


