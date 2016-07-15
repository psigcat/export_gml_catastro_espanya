# -*- coding: utf-8 -*-
"""Utilities that helps generating a spanish cadastre's GML plot file."""

from qgis.core import QGis, QgsMapLayer, QgsExpression
import time

# This function has inner functions to try to make the code more readable by starting with the most important functions.
def genereteCadastreGMLFile(layer, feature, path, area, date=None):
    """Generates a spanish cadastre's GML plot file.

    :param layer: Layer where the information comes from.
    :type layer: QgsMapLayer
    :param feature: Feature in the layer that contains the information to generate the file.
    :type feature: QgsFeature
    :param path: str or unicode
    :type path: str or unicode
    :param area: area that the user manually calcualted.
    :type area: str or unicode
    :param date: date of the modification (formatted 'yyyy-mm-dd'. Today if date is None.
    :type date: str, unicode or None
    """

    if layer.type() != QgsMapLayer.VectorLayer:
        raise ValueError(u'La capa seleccionada es de un tipo no procesable.')

    if date is None:
        date = time.strftime('%Y-%m-%d')

    crs = layer.crs().authid().split(':', 2);

    # If it is using an unkwown reference system, returns
    if crs[0] != 'EPSG':
        raise ValueError(u'El sistema de referencia de coordenadas es de un tipo no procesable')
    epsg = crs[1]

    # Get values from the feature atributes
    plotRef = feature["REFCAT"]
    muniCode = format(feature["DELEGACIO"], '02d') + format(feature["MUNICIPIO"], '03d')
    plotNum = feature["PARCELA"]
    
    # Get geometric attributes
    bounds = feature.geometry().boundingBox()
    min_xy = u'%f %f' % (bounds.xMinimum(), bounds.yMinimum()) 
    max_xy = u'%f %f' % (bounds.xMaximum(), bounds.yMaximum())
    centroid_xy = u'%f %f' % (QgsExpression('x(centroid($geometry))').evaluate(feature), QgsExpression('y(centroid($geometry))').evaluate(feature))
    vertex_count = '0'
    vertex_list = ''
    geometry = feature.geometry()

    # TODO (?) support more layers' geometric types
    if geometry.wkbType() == QGis.WKBPolygon:
        vertex = geometry.asPolygon()[0]
        vertex_count = str(len(vertex))

        try:
            iterator = iter(vertex)
            i = next(iterator)
            vertex_list = u'%f %f' % (i.x(), i.y())

            for i in iterator:
                vertex_list += u' %f %f' % (i.x(), i.y())

        except StopIteration:
            pass


    # Write the file
    with open(path, 'w+') as f:
        f.write(u'<?xml version="1.0" encoding="utf-8"?>\n')
        f.write(u'<!-- Archivo generado automaticamente por el plugin export_gm_cadastro_espanya de QGIS. -->\n')
        f.write(u'<!-- Parcela Catastral de la D.G. del Catastro. -->\n')
        f.write(u'<gml:FeatureCollection gml:id="ES.SDGC.CP" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:cp="urn:x-inspire:specification:gmlas:CadastralParcels:3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:x-inspire:specification:gmlas:CadastralParcels:3.0 http://inspire.ec.europa.eu/schemas/cp/3.0/CadastralParcels.xsd">\n')
        f.write(u'<gml:featureMember>\n')
        f.write(u'<cp:CadastralParcel gml:id="ES.SDGC.CP.' + plotRef + u'">\n')
        f.write(u'<gml:boundedBy>\n')
        f.write(u'<gml:Envelope srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n')
        f.write(u'  <gml:lowerCorner>' + min_xy + u'</gml:lowerCorner>\n')
        f.write(u'  <gml:upperCorner>' + max_xy + u'</gml:upperCorner>\n')
        f.write(u'</gml:Envelope>\n')
        f.write(u'</gml:boundedBy>\n')
        f.write(u'<cp:areaValue uom="m2">' + area + u'</cp:areaValue>\n')
        f.write(u'<cp:beginLifespanVersion>' + date + u'T00:00:00</cp:beginLifespanVersion>\n')
        f.write(u'<cp:endLifespanVersion xsi:nil="true" nilReason="other:unpopulated"></cp:endLifespanVersion>\n')
        f.write(u'<cp:geometry>\n')
        f.write(u'<gml:MultiSurface gml:id="MultiSurface_ES.SDGC.CP.' + plotRef + u'" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n')
        f.write(u'  <gml:surfaceMember>\n')
        f.write(u'  <gml:Surface gml:id="Surface_ES.SDGC.CP.' + plotRef + u'.1" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n')
        f.write(u'  <gml:patches>\n')
        f.write(u'  <gml:PolygonPatch>\n')
        f.write(u'  <gml:exterior>\n')
        f.write(u'      <gml:LinearRing>\n')
        f.write(u'          <gml:posList srsDimension="2" count="' + vertex_count + u'">' + vertex_list + u'</gml:posList>\n')
        f.write(u'      </gml:LinearRing>\n')
        f.write(u'  </gml:exterior>\n')
        f.write(u'  </gml:PolygonPatch>\n')
        f.write(u'  </gml:patches>\n')
        f.write(u'  </gml:Surface>\n')
        f.write(u'  </gml:surfaceMember>\n')
        f.write(u'</gml:MultiSurface>\n')
        f.write(u'</cp:geometry>\n')
        f.write(u'<cp:inspireId xmlns:base="urn:x-inspire:specification:gmlas:BaseTypes:3.2">\n')
        f.write(u'<base:Identifier>\n')
        f.write(u'  <base:localId>' + plotNum + u'</base:localId>\n')
        f.write(u'  <base:namespace>ES.LOCAL.CP</base:namespace>\n')
        f.write(u'</base:Identifier>\n')
        f.write(u'</cp:inspireId>\n')
        f.write(u'<cp:label>05</cp:label>\n')
        f.write(u'<cp:nationalCadastralReference>2</cp:nationalCadastralReference>\n')
        f.write(u'<cp:referencePoint>\n')
        f.write(u'<gml:Point gml:id="ReferencePoint_ES.SDGC.CP.' + plotRef + u'" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n')
        f.write(u'  <gml:pos>' + centroid_xy + u'</gml:pos>\n')
        f.write(u'</gml:Point>\n')
        f.write(u'</cp:referencePoint>\n')
        f.write(u'<cp:validFrom xsi:nil="true" nilReason="other:unpopulated"></cp:validFrom>\n')
        f.write(u'<cp:validTo xsi:nil="true" nilReason="other:unpopulated"></cp:validTo>\n')
        f.write(u'<cp:zoning xlink:href="#ES.SDGC.CP.Z.' + muniCode + u'U"></cp:zoning>\n')
        f.write(u'</cp:CadastralParcel>\n')
        f.write(u'</gml:featureMember>\n')
        f.write(u'<gml:featureMember>\n')
        f.write(u'<cp:CadastralZoning gml:id="ES.SDGC.CP.Z.' + muniCode + u'U">\n')
        f.write(u'<gml:boundedBy>\n')
        f.write(u'<gml:Envelope srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n')
        f.write(u'<gml:lowerCorner>' + min_xy + u'</gml:lowerCorner>\n')
        f.write(u'<gml:upperCorner>' + max_xy + u'</gml:upperCorner>\n')
        f.write(u'</gml:Envelope>\n')
        f.write(u'</gml:boundedBy>\n')
        f.write(u'<cp:beginLifespanVersion>' + date + u'T00:00:00</cp:beginLifespanVersion>\n')
        f.write(u'<cp:endLifespanVersion xsi:nil="true" nilReason="other:unpopulated"></cp:endLifespanVersion>\n')
        f.write(u'<cp:estimatedAccuracy uom="m">0.60</cp:estimatedAccuracy>\n')
        f.write(u'<cp:geometry>\n')
        f.write(u'<gml:MultiSurface gml:id="MultiSurface_ES.SDGC.CP.Z.' + muniCode + u'U" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n')
        f.write(u'<gml:surfaceMember>\n')
        f.write(u'<gml:Surface gml:id="Surface_ES.SDGC.CP.Z.' + muniCode + u'U.1" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n')
        f.write(u'<gml:patches>\n')
        f.write(u'<gml:PolygonPatch>\n')
        f.write(u'<gml:exterior>\n')
        f.write(u'<gml:LinearRing>\n')
        f.write(u'<gml:posList srsDimension="2" count="' + vertex_count + u'">' + vertex_list + u'</gml:posList>\n')
        f.write(u'</gml:LinearRing>\n')
        f.write(u'</gml:exterior>\n')
        f.write(u'</gml:PolygonPatch>\n')
        f.write(u'</gml:patches>\n')
        f.write(u'</gml:Surface>\n')
        f.write(u'</gml:surfaceMember>\n')
        f.write(u'</gml:MultiSurface>\n')
        f.write(u'</cp:geometry>\n')
        f.write(u'<cp:inspireId xmlns:base="urn:x-inspire:specification:gmlas:BaseTypes:3.2">\n')
        f.write(u'<base:Identifier>\n')
        f.write(u'<base:localId>' + muniCode + u'U</base:localId>\n')
        f.write(u'<base:namespace>ES.SDGC.CP.Z</base:namespace>\n')
        f.write(u'</base:Identifier>\n')
        f.write(u'</cp:inspireId>\n')
        f.write(u'<cp:label>' + muniCode + u'U</cp:label>\n')
        f.write(u'<cp:level codeSpace="urn:x-inspire:specification:gmlas:CadastralParcels:3.0/CadastralZoningLevelValue">1stOrder</cp:level>\n')
        f.write(u'<cp:levelName>\n')
        f.write(u'<gmd:LocalisedCharacterString locale="esp">MAPA</gmd:LocalisedCharacterString>\n')
        f.write(u'</cp:levelName>\n')
        f.write(u'<cp:nationalCadastalZoningReference>' + muniCode + u'U</cp:nationalCadastalZoningReference>\n')
        f.write(u'<cp:originalMapScaleDenominator>1000</cp:originalMapScaleDenominator>\n')
        f.write(u'<cp:referencePoint>\n')
        f.write(u'<gml:Point gml:id="ReferencePoint_ES.SDGC.CP.Z.X' + muniCode + u'U" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'"> \n')
        f.write(u'<gml:pos>' + centroid_xy + u'</gml:pos>\n')
        f.write(u'</gml:Point>\n')
        f.write(u'</cp:referencePoint>\n')
        f.write(u'<cp:validFrom xsi:nil="true" nilReason="unknown" />\n')
        f.write(u'<cp:validTo xsi:nil="true" nilReason="unknown" />\n')
        f.write(u'</cp:CadastralZoning>\n')
        f.write(u'</gml:featureMember>\n')
        f.write(u'</gml:FeatureCollection>\n')