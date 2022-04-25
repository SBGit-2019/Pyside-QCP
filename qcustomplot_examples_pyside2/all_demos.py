import sys
import os
from PySide2.QtWidgets import QApplication
from PySide2.QtCore import Qt, QCoreApplication

import qcustomplot_examples_pyside2.q_advancedaxesdemo
import qcustomplot_examples_pyside2.q_axistags
import qcustomplot_examples_pyside2.q_barchartdemo
import qcustomplot_examples_pyside2.q_colormapdemo
import qcustomplot_examples_pyside2.q_datedemo
import qcustomplot_examples_pyside2.q_financialdemo
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



def main():
    QCoreApplication.setAttribute(Qt.AA_ShareOpenGLContexts)
    app = QApplication(sys.argv)

    print("q_advancedaxesdemo")
    qcustomplot_examples_pyside2.q_advancedaxesdemo.demo(app)
    print("q_axistags")
    qcustomplot_examples_pyside2.q_axistags.demo(app)
    print("q_barchartdemo")
    qcustomplot_examples_pyside2.q_barchartdemo.demo(app)
    print("q_colormapdemo")
    qcustomplot_examples_pyside2.q_colormapdemo.demo(app)
    print("q_datedemo")
    qcustomplot_examples_pyside2.q_datedemo.demo(app)
    print("q_financialdemo")
    qcustomplot_examples_pyside2.q_financialdemo.demo(app)
    print("q_itemdemo")
    qcustomplot_examples_pyside2.q_itemdemo.demo(app)
    print("q_linestyledemo")
    qcustomplot_examples_pyside2.q_linestyledemo.demo(app)
    print("q_logarithmicdemo")
    qcustomplot_examples_pyside2.q_logarithmicdemo.demo(app)
    print("q_multiaxisdemo")
    qcustomplot_examples_pyside2.q_multiaxisdemo.demo(app)
    print("q_parametriccurvesdemo")
    qcustomplot_examples_pyside2.q_parametriccurvesdemo.demo(app)
    print("q_quadraticdemo")
    qcustomplot_examples_pyside2.q_quadraticdemo.demo(app)
    print("q_realtimedatademo")
    qcustomplot_examples_pyside2.q_realtimedatademo.demo(app)
    print("q_scatterpixmapdemo")
    qcustomplot_examples_pyside2.q_scatterpixmapdemo.demo(app)
    print("q_scatterstyledemo")
    qcustomplot_examples_pyside2.q_scatterstyledemo.demo(app)
    print("q_scrollbar_axis_range_control")
    qcustomplot_examples_pyside2.q_scrollbar_axis_range_control.demo(app)
    print("q_simpledemo")
    qcustomplot_examples_pyside2.q_simpledemo.demo(app)
    print("q_simpleitemdemo")
    qcustomplot_examples_pyside2.q_simpleitemdemo.demo(app)
    print("q_sincscatterdemo")
    qcustomplot_examples_pyside2.q_sincscatterdemo.demo(app)
    print("q_statisticaldemo")
    qcustomplot_examples_pyside2.q_statisticaldemo.demo(app)
    print("q_styleddemo")
    qcustomplot_examples_pyside2.q_styleddemo.demo(app)
    print("q_text_document_integration")
    qcustomplot_examples_pyside2.q_text_document_integration.demo(app)
    print("q_textinterface")
    qcustomplot_examples_pyside2.q_textinterface.demo(app)
    print("q_texturebrushdemo")
    qcustomplot_examples_pyside2.q_texturebrushdemo.demo(app)
    print("q_polarplotdemo")
    qcustomplot_examples_pyside2.q_polarplotdemo.demo(app)


if __name__ == '__main__':
    main()
    sys.exit(0)


