# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'D:\Data\Workspace\QGIS plugins\export_gml_catastro_espanya\ui\requestData_dialog.ui'
#
# Created: Fri Jul 15 18:02:37 2016
#      by: PyQt4 UI code generator 4.10.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_requestData_dialog(object):
    def setupUi(self, requestData_dialog):
        requestData_dialog.setObjectName(_fromUtf8("requestData_dialog"))
        requestData_dialog.resize(234, 150)
        requestData_dialog.setWindowTitle(_fromUtf8("Exportando parcela"))
        self.dialogLayout = QtGui.QVBoxLayout(requestData_dialog)
        self.dialogLayout.setObjectName(_fromUtf8("dialogLayout"))
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.parcela_lbl = QtGui.QLabel(requestData_dialog)
        self.parcela_lbl.setObjectName(_fromUtf8("parcela_lbl"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.parcela_lbl)
        self.area_lbl = QtGui.QLabel(requestData_dialog)
        self.area_lbl.setObjectName(_fromUtf8("area_lbl"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.area_lbl)
        self.area_dsb = QtGui.QDoubleSpinBox(requestData_dialog)
        self.area_dsb.setMaximum(9999.99)
        self.area_dsb.setSingleStep(5.0)
        self.area_dsb.setProperty("value", 100.0)
        self.area_dsb.setObjectName(_fromUtf8("area_dsb"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.area_dsb)
        self.diaEdicion_chb = QtGui.QCheckBox(requestData_dialog)
        self.diaEdicion_chb.setObjectName(_fromUtf8("diaEdicion_chb"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.diaEdicion_chb)
        self.diaEdicion_date = QtGui.QDateEdit(requestData_dialog)
        self.diaEdicion_date.setEnabled(False)
        self.diaEdicion_date.setObjectName(_fromUtf8("diaEdicion_date"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.diaEdicion_date)
        self.archivo_lbl = QtGui.QLabel(requestData_dialog)
        self.archivo_lbl.setObjectName(_fromUtf8("archivo_lbl"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.archivo_lbl)
        self.archivo_btn = QtGui.QPushButton(requestData_dialog)
        self.archivo_btn.setObjectName(_fromUtf8("archivo_btn"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.archivo_btn)
        self.parcela_tbx = QtGui.QLineEdit(requestData_dialog)
        self.parcela_tbx.setEnabled(False)
        self.parcela_tbx.setMouseTracking(False)
        self.parcela_tbx.setFocusPolicy(QtCore.Qt.NoFocus)
        self.parcela_tbx.setAcceptDrops(False)
        self.parcela_tbx.setFrame(False)
        self.parcela_tbx.setObjectName(_fromUtf8("parcela_tbx"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.parcela_tbx)
        self.dialogLayout.addLayout(self.formLayout)
        self.buttonBox = QtGui.QDialogButtonBox(requestData_dialog)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Save)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.dialogLayout.addWidget(self.buttonBox)

        self.retranslateUi(requestData_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), requestData_dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), requestData_dialog.reject)
        QtCore.QObject.connect(self.diaEdicion_chb, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.diaEdicion_date.setEnabled)
        QtCore.QMetaObject.connectSlotsByName(requestData_dialog)
        requestData_dialog.setTabOrder(self.area_dsb, self.archivo_btn)
        requestData_dialog.setTabOrder(self.archivo_btn, self.diaEdicion_chb)
        requestData_dialog.setTabOrder(self.diaEdicion_chb, self.diaEdicion_date)
        requestData_dialog.setTabOrder(self.diaEdicion_date, self.buttonBox)

    def retranslateUi(self, requestData_dialog):
        self.parcela_lbl.setText(_translate("requestData_dialog", "Parcela", None))
        self.area_lbl.setText(_translate("requestData_dialog", "Area (m²)", None))
        self.diaEdicion_chb.setText(_translate("requestData_dialog", "Dia de edición", None))
        self.archivo_lbl.setText(_translate("requestData_dialog", "Archivo a exportar", None))
        self.archivo_btn.setText(_translate("requestData_dialog", "...", None))
        self.parcela_tbx.setText(_translate("requestData_dialog", "0822805DF1802S", None))

