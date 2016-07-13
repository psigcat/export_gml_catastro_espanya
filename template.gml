<?xml version="1.0" encoding="utf-8"?>
<!--Parcela Catastral de la D.G. del Catastro.-->
<gml:FeatureCollection gml:id="ES.SDGC.CP" xmlns:gml="http://www.opengis.net/gml/3.2" xmlns:gmd="http://www.isotc211.org/2005/gmd" xmlns:ogc="http://www.opengis.net/ogc" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:cp="urn:x-inspire:specification:gmlas:CadastralParcels:3.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="urn:x-inspire:specification:gmlas:CadastralParcels:3.0 http://inspire.ec.europa.eu/schemas/cp/3.0/CadastralParcels.xsd">
<gml:featureMember>
<cp:CadastralParcel gml:id="ES.SDGC.CP.[% refcat %]">
<gml:boundedBy>
<gml:Envelope srsName="urn:ogc:def:crs:EPSG::25831">
  <gml:lowerCorner>[% xy_min %]</gml:lowerCorner>
  <gml:upperCorner>[% xy_max %]</gml:upperCorner>
</gml:Envelope>
</gml:boundedBy>
<cp:areaValue uom="m2">[% area %]</cp:areaValue>
<cp:beginLifespanVersion>2015-12-03T00:00:00</cp:beginLifespanVersion>
<cp:endLifespanVersion xsi:nil="true" nilReason="other:unpopulated"></cp:endLifespanVersion>
<cp:geometry>
<gml:MultiSurface gml:id="MultiSurface_ES.SDGC.CP.[% refcat %]" srsName="urn:ogc:def:crs:EPSG::[% epsg %]">
  <gml:surfaceMember>
  <gml:Surface gml:id="Surface_ES.SDGC.CP.[% refcat %].1" srsName="urn:ogc:def:crs:EPSG::[% epsg %]">
  <gml:patches>
  <gml:PolygonPatch>
  <gml:exterior>
      <gml:LinearRing>
          <gml:posList srsDimension="2" count="[% count_vertex %]">[% list_xy_vertex %]</gml:posList>
      </gml:LinearRing>
  </gml:exterior>
  </gml:PolygonPatch>
  </gml:patches>
  </gml:Surface>
  </gml:surfaceMember>
</gml:MultiSurface>
</cp:geometry>
<cp:inspireId xmlns:base="urn:x-inspire:specification:gmlas:BaseTypes:3.2">
<base:Identifier>
  <base:localId>[% number_newparcel %]</base:localId>
  <base:namespace>ES.LOCAL.CP</base:namespace>
</base:Identifier>
</cp:inspireId>
<cp:label>05</cp:label>
<cp:nationalCadastralReference>2</cp:nationalCadastralReference>
<cp:referencePoint>
<gml:Point gml:id="ReferencePoint_ES.SDGC.CP.[% refcat %]" srsName="urn:ogc:def:crs:EPSG::[% epsg %]">
  <gml:pos>[% xy_centroide %]</gml:pos>
</gml:Point>
</cp:referencePoint>
<cp:validFrom xsi:nil="true" nilReason="other:unpopulated"></cp:validFrom>
<cp:validTo xsi:nil="true" nilReason="other:unpopulated"></cp:validTo>
<cp:zoning xlink:href="#ES.SDGC.CP.Z.[% codi_muni %]U"></cp:zoning>
</cp:CadastralParcel>
</gml:featureMember>
<gml:featureMember>
<cp:CadastralZoning gml:id="ES.SDGC.CP.Z.[% codi_muni %]U">
<gml:boundedBy>
<gml:Envelope srsName="urn:ogc:def:crs:EPSG::[% epsg %]">
<gml:lowerCorner>[% xy_min %]</gml:lowerCorner>
<gml:upperCorner>[% xy_max %]</gml:upperCorner>
</gml:Envelope>
</gml:boundedBy>
<cp:beginLifespanVersion>2013-11-20T00:00:00</cp:beginLifespanVersion>
<cp:endLifespanVersion xsi:nil="true" nilReason="other:unpopulated"></cp:endLifespanVersion>
<cp:estimatedAccuracy uom="m">0.60</cp:estimatedAccuracy>
<cp:geometry>
<gml:MultiSurface gml:id="MultiSurface_ES.SDGC.CP.Z.[% codi_muni %]U" srsName="urn:ogc:def:crs:EPSG::[% epsg %]">
<gml:surfaceMember>
<gml:Surface gml:id="Surface_ES.SDGC.CP.Z.[% codi_muni %]U.1" srsName="urn:ogc:def:crs:EPSG::[% epsg %]">
<gml:patches>
<gml:PolygonPatch>
<gml:exterior>
<gml:LinearRing>
<gml:posList srsDimension="2" count="7">410716.56599998404 4582241.7116999887 410716.45877246361 4582245.4307895228 410721.80749998405 4582245.9224999873 410723.703499984 4582246.0839999868 410728.19864998397 4582246.4506999869 410728.38684998406 4582244.1440999871 410716.56599998404 4582241.7116999887</gml:posList>
</gml:LinearRing>
</gml:exterior>
</gml:PolygonPatch>
</gml:patches>
</gml:Surface>
</gml:surfaceMember>
</gml:MultiSurface>
</cp:geometry>
<cp:inspireId xmlns:base="urn:x-inspire:specification:gmlas:BaseTypes:3.2">
<base:Identifier>
<base:localId>[% codi_muni %]U</base:localId>
<base:namespace>ES.SDGC.CP.Z</base:namespace>
</base:Identifier>
</cp:inspireId>
<cp:label>[% codi_muni %]U</cp:label>
<cp:level codeSpace="urn:x-inspire:specification:gmlas:CadastralParcels:3.0/CadastralZoningLevelValue">1stOrder</cp:level>
<cp:levelName>
<gmd:LocalisedCharacterString locale="esp">MAPA</gmd:LocalisedCharacterString>
</cp:levelName>
<cp:nationalCadastalZoningReference>[% codi_muni %]U</cp:nationalCadastalZoningReference>
<cp:originalMapScaleDenominator>1000</cp:originalMapScaleDenominator>
<cp:referencePoint>
<gml:Point gml:id="ReferencePoint_ES.SDGC.CP.Z.X[% codi_muni %]U" srsName="urn:ogc:def:crs:EPSG::[% epsg %]"> 
<gml:pos>[% xy_centroide %]</gml:pos>
</gml:Point>
</cp:referencePoint>
<cp:validFrom xsi:nil="true" nilReason="unknown" />
<cp:validTo xsi:nil="true" nilReason="unknown" />
</cp:CadastralZoning>
</gml:featureMember>
</gml:FeatureCollection>
