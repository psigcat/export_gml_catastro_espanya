# This function has inner functions to try to make the code more readable by starting with the most important functions.
def genereteCadastreGMLFile(layer, feature, path, area):
    """Generates a spanish cadastre's update GML file

    :param layer: Layer where the information comes from.
    :type layer: QgsMapLayer
    :param feature: Feature in the layer that contains the information to generate the file.
    :type feature: QgsFeature
    :param path: str or unicode
    :type path: str or unicode
    :param area: area that the user manually calcualted.
    :type area: str or unicode
    """

    if iface.activeLayer().type() == QgsMapLayer.VectorLayer:
        raise ValueError(u'La capa seleccionada es de un tipo no procesable.')


    # Function which actually does the job.
    def generateFile(layer, feature, path, area):
        """Generates the file itself

        :param layer: layer where the information comes from.
        :type layer: QgsMapLayer
        :param feature: feature in the layer that contains the information to generate the file.
        :type feature: QgsFeature
        :param path: path of the file to write to (any current information will be removed)
        :type path: str or unicode
        :param area: area that the user manually calcualted.
        :type area: str or unicode
        """

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
        min_xy = "%f %f" % (bounds.xMinimum(), bounds.yMinimum()) 
        max_xy = "%f %f" % (bounds.xMaximum(), bounds.yMaximum())
        centroide_xy = "%f %f" % (QgsExpression('x(centroid($geometry))').evaluate(feature), QgsExpression('y(centroid($geometry))').evaluate(feature))
        vertex_count = 0
        vertex_list = ''
        geometry = feature.geometry()
        # TODO support more layers' geometric types
        if geometry.wkbType() == QGis.WKBPolygon:
            vertex = geometry.asPolygon()[0]
            vertex_count = len(vertex)

            try:
                iterator = iter(vertex)
                i = next(iterator)
                vertex_list = '%f %f' % (i.x(), i.y())

                for i in iterator:
                    vertex_list += ' %f %f' % (i.x(), i.y())

            except StopIteration:
                pass


        # Generate the string
        generated = genereteString(epsg, plotRef, muniCode, plotNum, area, min_xy, max_xy, centroide_xy, vertex_count, vertex_list)
        # Write the string into a file
        with open(path, 'r') as f:
            f.truncate()        # Removing if there was an older version of the file
            f.write(genereted)  # Writting the actual file


    # Generates the string that will be written to the file.
    def genereteString(epsg, plotRef, muniCode, plotNum, area, min_xy, max_xy, centroide_xy, vertex_count, vertex_list):
        """Generates the GML string which will be written to the file

        :param epsg: EPSG zone number.
        :type epsg: str or unicode
        :param plotRef: plot reference.
        :type plotRef: str or unicode
        :param muniCode: municipality code.
        :type muniCode: str or unicode
        :param plotNum: plot number (local).
        :type plotNum: str or unicode
        :param min_xy: point with the minimum x and y of the plot bounds (formatted as 'x y')
        :type min_xy: str or unicode
        :param max_xy: point with the maximum x and y of the plot bounds (formatted as 'x y')
        :type Max_xy: str or unicode
        :param centroide_x: the centroid point of the plot (formatted as 'x y')
        :type centroide_x: str or unicode
        :param vertex_count: number of vertex points
        :type vertex_count: str or unicode
        :param vertex_list: list of all the vertex points (formatted as 'x1 y1 x2 y2')
        """

        # This actually returns the file adding the parameters. 
        return u'\
<?xml version="1.0" encoding="utf-8"?>\n\
<!-- Archivo generado automaticamente por el plugin export_gm_cadastro_espanya de QGIS. -->\n\
<!-- Parcela Catastral de la D.G. del Catastro. -->\n\
<gml:FeatureCollection gml:id="ES.SDGC.CP" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:cp="urn:x-inspire:specification:gmlas:CadastralParcels:3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:x-inspire:specification:gmlas:CadastralParcels:3.0 http://inspire.ec.europa.eu/schemas/cp/3.0/CadastralParcels.xsd">\n\
<gml:featureMember>\n\
<cp:CadastralParcel gml:id="ES.SDGC.CP.' + plotRef + u'">\n\
<gml:boundedBy>\n\
<gml:Envelope srsName="urn:ogc:def:crs:EPSG::25831">\n\
  <gml:lowerCorner>' + min_xy + u'</gml:lowerCorner>\n\
  <gml:upperCorner>' + max_xy + u'</gml:upperCorner>\n\
</gml:Envelope>\n\
</gml:boundedBy>\n\
<cp:areaValue uom="m2">' + area + u'</cp:areaValue>\n\
<cp:beginLifespanVersion>2015-12-03T00:00:00</cp:beginLifespanVersion>\n\
<cp:endLifespanVersion xsi:nil="true" nilReason="other:unpopulated"></cp:endLifespanVersion>\n\
<cp:geometry>\n\
<gml:MultiSurface gml:id="MultiSurface_ES.SDGC.CP.' + plotRef + u'" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n\
  <gml:surfaceMember>\n\
  <gml:Surface gml:id="Surface_ES.SDGC.CP.' + plotRef + u'.1" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n\
  <gml:patches>\n\
  <gml:PolygonPatch>\n\
  <gml:exterior>\n\
      <gml:LinearRing>\n\
          <gml:posList srsDimension="2" count="' + vertex_count + u'">' + vertex_list + u'</gml:posList>\n\
      </gml:LinearRing>\n\
  </gml:exterior>\n\
  </gml:PolygonPatch>\n\
  </gml:patches>\n\
  </gml:Surface>\n\
  </gml:surfaceMember>\n\
</gml:MultiSurface>\n\
</cp:geometry>\n\
<cp:inspireId xmlns:base="urn:x-inspire:specification:gmlas:BaseTypes:3.2">\n\
<base:Identifier>\n\
  <base:localId>' + plotNum + u'</base:localId>\n\
  <base:namespace>ES.LOCAL.CP</base:namespace>\n\
</base:Identifier>\n\
</cp:inspireId>\n\
<cp:label>05</cp:label>\n\
<cp:nationalCadastralReference>2</cp:nationalCadastralReference>\n\
<cp:referencePoint>\n\
<gml:Point gml:id="ReferencePoint_ES.SDGC.CP.' + plotRef + u'" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n\
  <gml:pos>' + centroide_xy + u'</gml:pos>\n\
</gml:Point>\n\
</cp:referencePoint>\n\
<cp:validFrom xsi:nil="true" nilReason="other:unpopulated"></cp:validFrom>\n\
<cp:validTo xsi:nil="true" nilReason="other:unpopulated"></cp:validTo>\n\
<cp:zoning xlink:href="#ES.SDGC.CP.Z.' + muniCode + u'U"></cp:zoning>\n\
</cp:CadastralParcel>\n\
</gml:featureMember>\n\
<gml:featureMember>\n\
<cp:CadastralZoning gml:id="ES.SDGC.CP.Z.' + muniCode + u'U">\n\
<gml:boundedBy>\n\
<gml:Envelope srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n\
<gml:lowerCorner>' + min_xy + u'</gml:lowerCorner>\n\
<gml:upperCorner>' + max_xy + u'</gml:upperCorner>\n\
</gml:Envelope>\n\
</gml:boundedBy>\n\
<cp:beginLifespanVersion>2013-11-20T00:00:00</cp:beginLifespanVersion>\n\
<cp:endLifespanVersion xsi:nil="true" nilReason="other:unpopulated"></cp:endLifespanVersion>\n\
<cp:estimatedAccuracy uom="m">0.60</cp:estimatedAccuracy>\n\
<cp:geometry>\n\
<gml:MultiSurface gml:id="MultiSurface_ES.SDGC.CP.Z.' + muniCode + u'U" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n\
<gml:surfaceMember>\n\
<gml:Surface gml:id="Surface_ES.SDGC.CP.Z.' + muniCode + u'U.1" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n\
<gml:patches>\n\
<gml:PolygonPatch>\n\
<gml:exterior>\n\
<gml:LinearRing>\n\
<gml:posList srsDimension="2" count="7">410716.56599998404 4582241.7116999887 410716.45877246361 4582245.4307895228 410721.80749998405 4582245.9224999873 410723.703499984 4582246.0839999868 410728.19864998397 4582246.4506999869 410728.38684998406 4582244.1440999871 410716.56599998404 4582241.7116999887</gml:posList>\n\
</gml:LinearRing>\n\
</gml:exterior>\n\
</gml:PolygonPatch>\n\
</gml:patches>\n\
</gml:Surface>\n\
</gml:surfaceMember>\n\
</gml:MultiSurface>\n\
</cp:geometry>\n\
<cp:inspireId xmlns:base="urn:x-inspire:specification:gmlas:BaseTypes:3.2">\n\
<base:Identifier>\n\
<base:localId>' + muniCode + u'U</base:localId>\n\
<base:namespace>ES.SDGC.CP.Z</base:namespace>\n\
</base:Identifier>\n\
</cp:inspireId>\n\
<cp:label>' + muniCode + u'U</cp:label>\n\
<cp:level codeSpace="urn:x-inspire:specification:gmlas:CadastralParcels:3.0/CadastralZoningLevelValue">1stOrder</cp:level>\n\
<cp:levelName>\n\
<gmd:LocalisedCharacterString locale="esp">MAPA</gmd:LocalisedCharacterString>\n\
</cp:levelName>\n\
<cp:nationalCadastalZoningReference>' + muniCode + u'U</cp:nationalCadastalZoningReference>\n\
<cp:originalMapScaleDenominator>1000</cp:originalMapScaleDenominator>\n\
<cp:referencePoint>\n\
<gml:Point gml:id="ReferencePoint_ES.SDGC.CP.Z.X' + muniCode + u'U" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'"> \n\
<gml:pos>' + centroide_xy + u'</gml:pos>\n\
</gml:Point>\n\
</cp:referencePoint>\n\
<cp:validFrom xsi:nil="true" nilReason="unknown" />\n\
<cp:validTo xsi:nil="true" nilReason="unknown" />\n\
</cp:CadastralZoning>\n\
</gml:featureMember>\n\
</gml:FeatureCollection>'
    
    # ACTUAL FUNCTION CALL
    # Generating the file.
    generateFile(feature, filePath, area)