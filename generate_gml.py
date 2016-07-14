def genereteGMLFile(layer, feature, path):
    def generateFile(layer, feature, path):
        epsg = layer.crs().authid().split(':', 2)[1]
        refcat = feature["REFCAT"]
        codi_muni = format(feature["DELEGACIO"], '02d') + format(feature["MUNICIPIO"], '03d')
        parcel_num = feature["PARCELA"]
        
        bounds = feature.geometry().boundingBox()
        min_xy = "%f %f" % (bounds.xMinimum(), bounds.yMinimum()) 
        max_xy = "%f %f" % (bounds.xMaximum(), bounds.yMaximum())
        centroide_xy = "%f %f" % (QgsExpression('x(centroid($geometry))').evaluate(feature), QgsExpression('y(centroid($geometry))').evaluate(feature))
        
        vertex_count = 0
        vertex_list = ''
        if feature.wkbType() == QGis.WKBPolygon:
            vertex = feature.asPolygon()[0]
            vertex_count = vertex.length

            try:
                iterator = iter(vertex)
                i = next(iterator)
                vertex_list = '%f %f' % (i.x(), i.y())

                for i in iterator:
                    vertex_list += ' %f %f' % (i.x(), i.y())

            except StopIteration:
                pass



        generated = genereteString(epsg, refcat, codi_muni, parcel_num, min_xy, max_xy, centroide_xy, vertex_count, vertex_list)
        with open(path, 'r') as f:
            f.truncate()
            f.write(genereted)



    def genereteString(epsg, refcat, codi_muni, parcel_num, min_xy, max_xy, centroide_xy, vertex_count, vertex_list):
      return u'<!-- Archivo generado automaticamente por el plugin export_gm_cadastro_espanya de QGIS -->\n\
<?xml version="1.0" encoding="utf-8"?>\n\
<!--Parcela Catastral de la D.G. del Catastro.-->\n\
<gml:FeatureCollection gml:id="ES.SDGC.CP" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:cp="urn:x-inspire:specification:gmlas:CadastralParcels:3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:x-inspire:specification:gmlas:CadastralParcels:3.0 http://inspire.ec.europa.eu/schemas/cp/3.0/CadastralParcels.xsd">\n\
<gml:featureMember>\n\
<cp:CadastralParcel gml:id="ES.SDGC.CP.' + refcat + u'">\n\
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
<gml:MultiSurface gml:id="MultiSurface_ES.SDGC.CP.' + refcat + u'" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n\
  <gml:surfaceMember>\n\
  <gml:Surface gml:id="Surface_ES.SDGC.CP.' + refcat + u'.1" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n\
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
  <base:localId>' + parcel_num + u'</base:localId>\n\
  <base:namespace>ES.LOCAL.CP</base:namespace>\n\
</base:Identifier>\n\
</cp:inspireId>\n\
<cp:label>05</cp:label>\n\
<cp:nationalCadastralReference>2</cp:nationalCadastralReference>\n\
<cp:referencePoint>\n\
<gml:Point gml:id="ReferencePoint_ES.SDGC.CP.' + refcat + u'" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n\
  <gml:pos>' + centroide_xy + u'</gml:pos>\n\
</gml:Point>\n\
</cp:referencePoint>\n\
<cp:validFrom xsi:nil="true" nilReason="other:unpopulated"></cp:validFrom>\n\
<cp:validTo xsi:nil="true" nilReason="other:unpopulated"></cp:validTo>\n\
<cp:zoning xlink:href="#ES.SDGC.CP.Z.' + codi_muni + u'U"></cp:zoning>\n\
</cp:CadastralParcel>\n\
</gml:featureMember>\n\
<gml:featureMember>\n\
<cp:CadastralZoning gml:id="ES.SDGC.CP.Z.' + codi_muni + u'U">\n\
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
<gml:MultiSurface gml:id="MultiSurface_ES.SDGC.CP.Z.' + codi_muni + u'U" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n\
<gml:surfaceMember>\n\
<gml:Surface gml:id="Surface_ES.SDGC.CP.Z.' + codi_muni + u'U.1" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'">\n\
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
<base:localId>' + codi_muni + u'U</base:localId>\n\
<base:namespace>ES.SDGC.CP.Z</base:namespace>\n\
</base:Identifier>\n\
</cp:inspireId>\n\
<cp:label>' + codi_muni + u'U</cp:label>\n\
<cp:level codeSpace="urn:x-inspire:specification:gmlas:CadastralParcels:3.0/CadastralZoningLevelValue">1stOrder</cp:level>\n\
<cp:levelName>\n\
<gmd:LocalisedCharacterString locale="esp">MAPA</gmd:LocalisedCharacterString>\n\
</cp:levelName>\n\
<cp:nationalCadastalZoningReference>' + codi_muni + u'U</cp:nationalCadastalZoningReference>\n\
<cp:originalMapScaleDenominator>1000</cp:originalMapScaleDenominator>\n\
<cp:referencePoint>\n\
<gml:Point gml:id="ReferencePoint_ES.SDGC.CP.Z.X' + codi_muni + u'U" srsName="urn:ogc:def:crs:EPSG::' + epsg + u'"> \n\
<gml:pos>' + centroide_xy + u'</gml:pos>\n\
</gml:Point>\n\
</cp:referencePoint>\n\
<cp:validFrom xsi:nil="true" nilReason="unknown" />\n\
<cp:validTo xsi:nil="true" nilReason="unknown" />\n\
</cp:CadastralZoning>\n\
</gml:featureMember>\n\
</gml:FeatureCollection>'


    if iface.activeLayer().type() == QgsMapLayer.VectorLayer:
        generateFile(feature, filePath)