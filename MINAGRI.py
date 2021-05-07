import sys, os
from osgeo import ogr, gdal

# Params
_OUT_DIR = r'/home/luisamos/Descargas'
_GEOMETRY_TYPE = 'polygon'     # options: point, line, polygon
_WFS_URL = 'https://geo.minagri.gob.pe/arcgis/services/servicios_ogc/Peru_midagri_1502/MapServer/WFSServer?'
#_WFS_URL = 'https://geo.minagri.gob.pe/arcgis/services/servicios_ogc/Peru_midagri_1501_puno/MapServer/WFSServer'

driver_wfs = ogr.GetDriverByName('WFS')
#gdal.SetConfigOption('GDAL_HTTP_UNSAFESSL', 'YES')
#gdal.SetConfigOption('INVERT_AXIS_ORDER_IF_LAT_LONG', 'NO')
#gdal.SetConfigOption('GDAL_IGNORE_AXIS_ORIENTATION', 'NO')
gdal.SetConfigOption('GML_INVERT_AXIS_ORDER_IF_LAT_LONG', 'NO')


wfs = driver_wfs.Open('WFS:' + _WFS_URL)

layer_count = wfs.GetLayerCount()

for i in range(layer_count):
    layer = wfs.GetLayerByIndex(i)
    layer_name = layer.GetName()
    driver_shapefile = ogr.GetDriverByName('ESRI Shapefile')
    nombre_shp = layer_name + '.shp'
    out_feature = os.path.join(_OUT_DIR, nombre_shp)
    data_source = driver_shapefile.CreateDataSource(out_feature)
    prj = layer.GetSpatialRef()
    
    if _GEOMETRY_TYPE == 'point':
        geom = ogr.wkbPoint
    elif _GEOMETRY_TYPE == 'line':
        geom = ogr.wkbLineString
    elif _GEOMETRY_TYPE == 'polygon':
        geom = ogr.wkbPolygon
    layer_new = data_source.CreateLayer(layer_name, prj, geom)
    layer_def = layer.GetLayerDefn()
    total_registros = layer_def.GetFieldCount()
    print("Total de registros: "+ str(total_registros))
    for field in range(total_registros):
        field_name = layer_def.GetFieldDefn(field).GetName()
        if field_name in ('SHAPE.STArea__', 'SHAPE.STLength__'):
            continue
        layer_new.CreateField(layer_def.GetFieldDefn(field))
    i=0
    for row in layer:
    	layer_new.CreateFeature(row)
    	i=i+1
    	print("Insertando registro: "+str(i))

    print("Finalizado")       