# -*- coding: utf-8 -*-
"""
/***************************************************************************
 export_gml_catastro_espanya - A QGIS plugin that creates GML files of plots for the spainish catastre
                             -------------------
        begin                : 2016-06-29
        copyright            : (C) 2016 by Martí Angelats
        email                : martiangelats@hotmail.com
        git sha              : $Format:%H$
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
 This script initializes the plugin, making it known to QGIS.
"""


# noinspection PyPep8Naming
def classFactory(iface):  # pylint: disable=invalid-name
    """Load export_gml_catastro_espanya class from file export_gml_catastro_espanya.

    :param iface: A QGIS interface instance.
    :type iface: QgsInterface
    """
    #
    from .search_plus import export_gml_catastro_espanya
    return export_gml_catastro_espanya(iface)
