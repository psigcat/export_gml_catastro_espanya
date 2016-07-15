# -*- coding: utf-8 -*-
"""

"""

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from generate_gml import genereteCadastreGMLFile
from ui.requestData_dialog import Ui_requestData_dialog



class export_gml_catastro_espanya:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
        # Find icon
        path = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.abspath(os.path.join(path, 'icon_export_gml_catastro_espanya.png'))

        self.action = QAction(QIcon(str(filename)), "export_gml_catastro_espanya", self.iface.mainWindow())
        self.action.setObjectName("testAction")
        self.action.setWhatsThis("Configuration for test plugin")
        self.action.setStatusTip("This is status tip")
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)

        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu("Testing pluging", self.action)


    def unload(self):
        self.iface.removePluginMenu("Testing pluging", self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        # Check for a correct layer
        layer = self.iface.activeLayer()
        if layer == None:
            return # no layer detected
        if layer.type() != QgsMapLayer.VectorLayer: # TODO (?) add more conditions
            return # TODO show error popup

        # Check that there is, at least, a single feature selected
        features = layer.selectedFeatures()
        if len(features) <= 0:
            return # TODO show error popup

        #TODO (?) iterate features
        feature = features[0]

        # popup dialog
        dialog = QDialog()
        dialog.ui = Ui_requestData_dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(Qt.WA_DeleteOnClose)

        # set parcela_tbx text to the plot's reference
        dialog.ui.parcela_tbx.setText(feature['REFCAT'])

        # set default date to today
        dialog.ui.diaEdicion_date.setDate(QDate.currentDate())

        # variable shared with the inner function (file choose dialog)
        class nonlocal:
            path = None

        # defining and connectiong the archivo_btn clicked() signal
        def openFileButtonClick():
            filename = QFileDialog.getSaveFileName(dialog, "Save File", feature['REFCAT']+".gml", "Geography Markup Language File (*.gml)");
            if filename != "":
                nonlocal.path = filename
                dialog.ui.archivo_btn.setText(filename);
        QObject.connect(dialog.ui.archivo_btn, SIGNAL("clicked()"), openFileButtonClick)

        def dialogAccepted():
            if nonlocal.path != None and nonlocal.path != "":
                if dialog.ui.diaEdicion_chb.isChecked():
                    date = dialog.ui.diaEdicion_date.date()
                else:
                    date = QDate.currentDate()
                date_s = "%04i-%02i-%02i" % (date.year(), date.month(), date.day())
                area_s = "%.5f" % dialog.ui.area_dsb.value()
                genereteCadastreGMLFile(layer, feature, nonlocal.path, area_s, date_s)

        QObject.connect(dialog, SIGNAL("accepted()"), dialogAccepted)

        # execute the dialog execute loop (waits for the result)
        dialog.exec_()


