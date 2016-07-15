# -*- coding: utf-8 -*-
"""

"""

import os
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

class export_gml_catastro_espanya:
    def __init__(self, iface):
        self.iface = iface

    def initGui(self):
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
        print "Hello World!"