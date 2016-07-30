# -*- coding: utf-8 -*-
"""

"""

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from generate_gml import genereteCadastreGMLFile
from ui.requestData_dialog import Ui_requestData_dialog


# Unicode QString generator function
try:
    qu = QtCore.QString.fromUtf8
except AttributeError:
    def qu(s):
        return s

# Translate function
try:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, QtGui.QApplication.UnicodeUTF8)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

def tr(text):
    return _translate("export_gml_catastro_espanya", text, None)

# TODO documentation

class export_gml_catastro_espanya:
    def __init__(self, iface):
        self.iface = iface

        # Get the settings
        self.settings = QSettings("PSIG", "export_gml_catastro_espanya")

        # Find and safe icon
        path = os.path.dirname(os.path.abspath(__file__))
        filename = os.path.abspath(os.path.join(path, 'icon_export_gml_catastro_espanya.png'))
        self.icon = QIcon(str(filename))


    def initGui(self):
        # Add menu and toolbar entries
        self.action = QAction(self.icon, tr("Generar GML para el catastro español"), self.iface.mainWindow())
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(qu("Export GML catastro de España"), self.action)


    def unload(self):
        # Remove menu and toolbar entries
        self.iface.removePluginMenu(qu("Export GML catastro de España"), self.action)
        self.iface.removeToolBarIcon(self.action)

    def run(self):
        layer = self.iface.activeLayer()

        # if the selected layer is not of the correct type, do nothing and end
        if layer == None or layer.type() != QgsMapLayer.VectorLayer:
            return

        features = layer.selectedFeatures()

        # if there is not one (and only one) feature sleected, do nothing and end
        if len(features) != 1:
            return

        feature = features[0]

        # Safe the references of the used feature fields
        refcatIndex = feature.fieldNameIndex('REFCAT')
        delegacioIndex = feature.fieldNameIndex('DELEGACIO')
        municipioIndex = feature.fieldNameIndex('MUNICIPIO')

        # Get splitted crs
        crs = layer.crs().authid().split(':', 2);


        # This fields are always present in the spanish cadastre files.
        #   If they do not exist or the CRS is not EPGS, it means that the gml file cannot be generated.
        #   If so, popup an error and end (there may be an error in the map, so feedback is required)
        if crs[0] != 'EPSG':
            self.__errorPopup(tr("La capa seleccionada no utiliza un sistema de coodenadas compatible."))
            return
        if refcatIndex < 0 or refcatIndex < 0 or refcatIndex < 0:
            self.__errorPopup(tr("La capa selccionada no contiene los campos necesarios."))
            return

        geometry = feature.geometry()

        # Check for non-implemented geometry WKB types
        if geometry.wkbType() != QGis.WKBPolygon:
            self.__errorPopup(tr("Tipo de WKB no compatible."))
            return

        # Set epsg type to the second part of the crs
        epsg = crs[1]

        # popup dialog
        dialog = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        dialog.ui = Ui_requestData_dialog()
        dialog.ui.setupUi(dialog)
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowIcon(self.icon)

        # set parcela_tbx text to the plot's reference
        dialog.ui.parcela_tbx.setText(feature[refcatIndex])

        # set default date to today
        dialog.ui.diaEdicion_de.setDate(QDate.currentDate())

        # allow disable the date and resets to the original value (today)
        def toggleDE(b):
            dialog.ui.diaEdicion_de.setEnabled(b)
            if not b:
                dialog.ui.diaEdicion_de.setDate(QDate.currentDate())

        QObject.connect(dialog.ui.diaEdicion_chb, SIGNAL("toggled(bool)"), toggleDE)

        # if dialog accepted (popup save file dialog)
        def saveButtonClicked():
            dialog.setVisible(False)
            path = QFileDialog.getSaveFileName(
                dialog,
                None,
                os.path.join(
                    self.settings.value("save path", os.path.expanduser("~")),      #default folder
                    feature[refcatIndex]+"_"+dialog.ui.num_parcel_tbx.text()+".gml" #default filename
                ),
                "Geography Markup Language File (*.gml)"
            )

            # If the path is possible
            if path != None and path != "":
                # safe the folder path in the settings for the next time
                self.settings.setValue("save path", os.path.dirname(path))

                # temporal variables
                bounds = geometry.boundingBox()
                date_value = dialog.ui.diaEdicion_de.date()
                vertex = getVertex(geometry)

                # Generate all the necesary arguments to generate the file (in order of function argument)
                # path
                # epsg
                muniCode = format(feature[delegacioIndex], '02d') + format(feature[municipioIndex], '03d')
                plotNum = str(dialog.ui.num_parcel_tbx.text())
                plotRef = feature[refcatIndex]
                centroid_xy = u'%f %f' % (
                    QgsExpression('x(centroid($geometry))').evaluate(feature),
                    QgsExpression('y(centroid($geometry))').evaluate(feature)
                )
                min_xy = u'%f %f' % (bounds.xMinimum(), bounds.yMinimum()) 
                max_xy = u'%f %f' % (bounds.xMaximum(), bounds.yMaximum())
                area = "%.5f" % dialog.ui.area_dsb.value()
                date = "%04i-%02i-%02i" % (date_value.year(), date_value.month(), date_value.day())
                vertex_count = str(len(vertex))
                vertex_list = ''
                try:
                    iterator = iter(vertex)
                    i = next(iterator)
                    vertex_list = u'%f %f' % (i.x(), i.y())
                    for i in iterator:
                        vertex_list += u' %f %f' % (i.x(), i.y())
                except StopIteration:
                    # if there are no vertex, do nothing
                    pass

                genereteCadastreGMLFile(path, epsg, muniCode, plotNum, plotRef, centroid_xy, min_xy, max_xy, area, date, vertex_count, vertex_list)
                dialog.accept()
            
            else:
                dialog.reject()

        QObject.connect(dialog.ui.save_btn, SIGNAL("clicked()"), saveButtonClicked)

        # execute the dialog execute loop (waits for the result)
        dialog.exec_()

    def __errorPopup(self, msg):
        messageBox = QMessageBox(QMessageBox.Critical, tr("Error"), msg)
        messageBox.setWindowIcon(self.icon)
        messageBox.exec_()


def getVertex(geometry):

    # possible TODO add more geometry wkbTypes support
    if geometry.wkbType() == QGis.WKBPolygon:
        return geometry.asPolygon()[0]
    else:
        # If it is not a supported type, return an empty list
        return []
