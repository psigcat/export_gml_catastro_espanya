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
        self.settings = QSettings("PSIG", "export_gml_catastro_espanya")

        # Find and safe icon
        path = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.abspath(os.path.join(path, 'icon_export_gml_catastro_espanya.png'))
        self.icon = QIcon(str(filename))


    def initGui(self):
        self.action = QAction(self.icon, u"Export GML catastro de España", self.iface.mainWindow())
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
            return # TODO (?) show error popup

        # Check that there is, at least, a single feature selected
        features = layer.selectedFeatures()
        if len(features) <= 0:
            return # TODO (?) show error popup

        #TODO (?) iterate features
        feature = features[0]

        # popup dialog
        dialog = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        dialog.ui = Ui_requestData_dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowIcon(self.icon)

        # set parcela_tbx text to the plot's reference
        dialog.ui.parcela_tbx.setText(feature['REFCAT'])

        # set default date to today
        dialog.ui.diaEdicion_de.setDate(QDate.currentDate())

        # allow disable the date and resets to the original value (today)
        def toggleDE(b):
            dialog.ui.diaEdicion_de.setEnabled(b)
            if not b:
                dialog.ui.diaEdicion_de.setDate(QDate.currentDate())

        QObject.connect(dialog.ui.diaEdicion_chb, SIGNAL("toggled(bool)"), toggleDE)

        # if dialog accepted
        def saveButtonClicked():
            dialog.setVisible(False)
            path = QFileDialog.getSaveFileName(
                dialog,
                "Save File",
                os.path.join(
                    self.settings.value("save path", os.path.expanduser("~")),      #default folder
                    feature['REFCAT']+"_"+dialog.ui.num_parcel_tbx.text()+".gml"    #default filename
                ),
                "Geography Markup Language File (*.gml)"
            )

            if path != None and path != "":
                self.settings.setValue("save path", os.path.dirname(path))

                area_s = "%.5f" % dialog.ui.area_dsb.value()
                plot_num_s = str(dialog.ui.num_parcel_tbx.text())
                date = dialog.ui.diaEdicion_de.date()
                date_s = "%04i-%02i-%02i" % (date.year(), date.month(), date.day())

                genereteCadastreGMLFile(layer, feature, path, area_s, plot_num_s, date_s)
                dialog.accept()
            else:
                dialog.reject()

        QObject.connect(dialog.ui.save_btn, SIGNAL("clicked()"), saveButtonClicked)

        # execute the dialog execute loop (waits for the result)
        dialog.exec_()


