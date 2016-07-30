# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'requestData_dialog.ui'
#
# Created: Sat Jul 30 12:18:13 2016
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
        requestData_dialog.resize(339, 314)
        requestData_dialog.setWindowTitle(_fromUtf8("Exportando parcela"))
        requestData_dialog.setStyleSheet(_fromUtf8("font: 10pt \"Georgia\";"))
        self.verticalLayout = QtGui.QVBoxLayout(requestData_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.verticalLayout_3 = QtGui.QVBoxLayout()
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.label = QtGui.QLabel(requestData_dialog)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Georgia"))
        font.setPointSize(10)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(50)
        self.label.setFont(font)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_3.addWidget(self.label)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.formLayout = QtGui.QFormLayout()
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.refcat_lbl = QtGui.QLabel(requestData_dialog)
        self.refcat_lbl.setObjectName(_fromUtf8("refcat_lbl"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.LabelRole, self.refcat_lbl)
        self.parcela_tbx = QtGui.QLineEdit(requestData_dialog)
        self.parcela_tbx.setEnabled(False)
        self.parcela_tbx.setMouseTracking(False)
        self.parcela_tbx.setFocusPolicy(QtCore.Qt.NoFocus)
        self.parcela_tbx.setAcceptDrops(False)
        self.parcela_tbx.setFrame(False)
        self.parcela_tbx.setObjectName(_fromUtf8("parcela_tbx"))
        self.formLayout.setWidget(0, QtGui.QFormLayout.FieldRole, self.parcela_tbx)
        self.num_parcel_lbl = QtGui.QLabel(requestData_dialog)
        self.num_parcel_lbl.setObjectName(_fromUtf8("num_parcel_lbl"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.LabelRole, self.num_parcel_lbl)
        self.num_parcel_tbx = QtGui.QLineEdit(requestData_dialog)
        self.num_parcel_tbx.setObjectName(_fromUtf8("num_parcel_tbx"))
        self.formLayout.setWidget(1, QtGui.QFormLayout.FieldRole, self.num_parcel_tbx)
        self.area_lbl = QtGui.QLabel(requestData_dialog)
        self.area_lbl.setObjectName(_fromUtf8("area_lbl"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.LabelRole, self.area_lbl)
        self.area_dsb = QtGui.QDoubleSpinBox(requestData_dialog)
        self.area_dsb.setMaximum(9999.99)
        self.area_dsb.setSingleStep(5.0)
        self.area_dsb.setProperty("value", 100.0)
        self.area_dsb.setObjectName(_fromUtf8("area_dsb"))
        self.formLayout.setWidget(2, QtGui.QFormLayout.FieldRole, self.area_dsb)
        self.diaEdicion_chb = QtGui.QCheckBox(requestData_dialog)
        self.diaEdicion_chb.setObjectName(_fromUtf8("diaEdicion_chb"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.LabelRole, self.diaEdicion_chb)
        self.diaEdicion_de = QtGui.QDateEdit(requestData_dialog)
        self.diaEdicion_de.setEnabled(False)
        self.diaEdicion_de.setCalendarPopup(True)
        self.diaEdicion_de.setObjectName(_fromUtf8("diaEdicion_de"))
        self.formLayout.setWidget(3, QtGui.QFormLayout.FieldRole, self.diaEdicion_de)
        self.verticalLayout.addLayout(self.formLayout)
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setSpacing(3)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.save_btn = QtGui.QPushButton(requestData_dialog)
        self.save_btn.setObjectName(_fromUtf8("save_btn"))
        self.horizontalLayout.addWidget(self.save_btn)
        self.cancel_btn = QtGui.QPushButton(requestData_dialog)
        self.cancel_btn.setObjectName(_fromUtf8("cancel_btn"))
        self.horizontalLayout.addWidget(self.cancel_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(requestData_dialog)
        QtCore.QObject.connect(self.cancel_btn, QtCore.SIGNAL(_fromUtf8("clicked()")), requestData_dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(requestData_dialog)

    def retranslateUi(self, requestData_dialog):
        self.label.setText(_translate("requestData_dialog", "HERRAMIENTA PARA EXPORTAR A GML", None))
        self.refcat_lbl.setText(_translate("requestData_dialog", "Refcat", None))
        self.parcela_tbx.setText(_translate("requestData_dialog", "0822805DF1802S", None))
        self.num_parcel_lbl.setText(_translate("requestData_dialog", "Numero parcela", None))
        self.area_lbl.setText(_translate("requestData_dialog", "Area (m²)", None))
        self.diaEdicion_chb.setText(_translate("requestData_dialog", "Dia de edición", None))
        self.save_btn.setText(_translate("requestData_dialog", "Guardar...", None))
        self.cancel_btn.setText(_translate("requestData_dialog", "Cancelar", None))

