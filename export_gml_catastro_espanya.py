# -*- coding: utf-8 -*-
"""
"""
# TODO documentation

import os
from PyQt4 import QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from generate_gml import genereteCadastreGMLFile
from ui.requestData_dialog import Ui_requestData_dialog


# Main plugin's class (where all the magic happens)
class export_gml_catastro_espanya:
    def __init__(self, iface):
        # Save the plugin's name and the path to the containing folder
        self.plugin_dir = os.path.dirname(__file__)
        self.pluginName = os.path.basename(self.plugin_dir)

        # Safe the QGIS iface
        self.iface = iface

        # Translate, if a translation exist, to the local language
        locale = QSettings().value('locale/userLocale')[0:2]
        locale_path = os.path.join(self.plugin_dir, 'i18n', 'export_gml_catastro_espanya_{}.qm'.format(locale))
        if os.path.exists(locale_path):
            self.translator = QTranslator()
            self.translator.load(locale_path)
            if qVersion() > '4.3.3':
                QCoreApplication.installTranslator(self.translator)


        # Get the QSettings (saves configuration)
        self.settings = QSettings("PSIG", "export_gml_catastro_espanya")

        # Find and safe the plugin's icon
        filename = os.path.abspath(os.path.join(self.plugin_dir, 'icon_export_gml_catastro_espanya.png'))
        self.icon = QIcon(str(filename))


    def initGui(self):
        # Add menu and toolbar entries (basically allows to activate it)
        self.action = QAction(self.icon, tr("Generar GML para el catastro español"), self.iface.mainWindow())
        QObject.connect(self.action, SIGNAL("triggered()"), self.run)
        self.iface.addToolBarIcon(self.action)
        self.iface.addPluginToMenu(qu("Export GML catastro de España"), self.action)


    def unload(self):
        # Remove menu and toolbar entries
        self.iface.removePluginMenu(qu("Export GML catastro de España"), self.action)
        self.iface.removeToolBarIcon(self.action)

    # Called when the user clicks the icon or the menu entry
    def run(self):
        # Gets the selected layer
        layer = self.iface.activeLayer()

        # If the selected layer is not the correct type, do nothing and return
        if layer == None or layer.type() != QgsMapLayer.VectorLayer:
            return

        # Get the selected feature AKA plot). Only a single one (end if there are none or more).
        features = layer.selectedFeatures()
        if len(features) != 1:
            return
        feature = features[0]

        # Safe the references of the used feature fields
        delegacionIndex = feature.fieldNameIndex('DELEGACIO')
        municipioIndex = feature.fieldNameIndex('MUNICIPIO')
        refcatIndex = feature.fieldNameIndex('REFCAT')

        # If the feature REFCAT doesn't exist, it is possible that is split into two features: pcat1 and pcat2
        if refcatIndex < 0:
            try:
                refcat = feature['pcat1'] +  feature['pcat2']
            except KeyError:
                refcat = None
        else:
            refcat = feature[refcatIndex]


        # This fields are always present in the spanish cadastre files.
        #   If they do not exist or the CRS is not EPGS, it means that the gml file cannot be generated.
        #   If so, popup an error and return (there may be an error in the map, so feedback is required)
        crs = layer.crs().authid().split(':', 2);
        if crs[0] != 'EPSG':
            self.__errorPopup(tr("La capa seleccionada no utiliza un sistema de coodenadas compatible."))
            return


        # Check for non-implemented geometry WKB types
        geometry = feature.geometry()
        if geometry.wkbType() != QGis.WKBPolygon:
            self.__errorPopup(tr("Tipo de WKB no compatible."))
            return

        # Set epsg type to the second part of the crs
        epsg = crs[1]

        # Setting the options' popup dialog
        dialog = QDialog(None, Qt.WindowSystemMenuHint | Qt.WindowTitleHint)
        dialog.ui = Ui_requestData_dialog()
        dialog.ui.setupUi(dialog)
        dialog.setWindowTitle(_translate("requestData_dialog", "Exportando parcela", None))
        dialog.setAttribute(Qt.WA_DeleteOnClose)
        dialog.setWindowIcon(self.icon)

        # If we already have the values of the textboxes, fill and disable them.
        if refcat is not None:
            dialog.ui.parcela_tbx.setEnabled(False)
            dialog.ui.parcela_tbx.setText(refcat)

        if delegacionIndex >= 0:
            dialog.ui.deleg_tbx.setEnabled(False)
            dialog.ui.deleg_tbx.setText(str(feature[delegacionIndex]))

        if municipioIndex >= 0:
            dialog.ui.muni_tbx.setEnabled(False)
            dialog.ui.muni_tbx.setText(str(feature[municipioIndex]))


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
                    refcat+"_"+dialog.ui.num_parcel_tbx.text()+".gml" #default filename
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
                muniCode = format(feature[delegacionIndex], '02d') + format(feature[municipioIndex], '03d')
                plotNum = str(dialog.ui.num_parcel_tbx.text())
                plotRef = refcat
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


    # Popups an error (utility)
    def __errorPopup(self, msg):
        messageBox = QMessageBox(QMessageBox.Critical, tr("Error"), msg)
        messageBox.setWindowIcon(self.icon)
        messageBox.exec_()




# Utilities

# Unicode QString generator function
try:
    qu = QtCore.QString.fromUtf8
except AttributeError:
    def qu(s):
        return s

# Qt translate function
try:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig, QApplication.UnicodeUTF8)
except AttributeError:
    def _translate(context, text, disambig):
        return QApplication.translate(context, text, disambig)
def tr(text):
    return _translate("export_gml_catastro_espanya", text, None)


# Returns the vertex of the geometry object
def getVertex(geometry):
    # possible TODO add more geometry wkbTypes support
    if geometry.wkbType() == QGis.WKBPolygon:
        return geometry.asPolygon()[0]
    else:
        # If it is not a supported type, return an empty list
        return []
