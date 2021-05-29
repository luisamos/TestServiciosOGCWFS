import sys, os
from osgeo import ogr, gdal
from datetime import datetime

# Parametros
ruta_descarga = r'/apps/python'
tipo_geometria = 'polygon'     # options: point, line, polygon
url_wfs = 'https://geo.minagri.gob.pe/arcgis/services/servicios_ogc/Peru_midagri_1502/MapServer/WFSServer?VERSION=1.0.0&MAXFEATURES=1489'
#url_wfs = 'https://geo.minagri.gob.pe/arcgis/services/servicios_ogc/Peru_midagri_1501_puno/MapServer/WFSServer?'

driver_wfs = ogr.GetDriverByName('WFS')
#gdal.SetConfigOption('GDAL_HTTP_UNSAFESSL', 'YES')
#gdal.SetConfigOption('INVERT_AXIS_ORDER_IF_LAT_LONG', 'NO')
#gdal.SetConfigOption('GDAL_IGNORE_AXIS_ORIENTATION', 'NO')
gdal.SetConfigOption('GML_INVERT_AXIS_ORDER_IF_LAT_LONG', 'NO')

wfs = driver_wfs.Open('WFS:' + url_wfs)
#wfs = driver_wfs.Open('WFS:'+ url_wfs)
total_capas = wfs.GetLayerCount()
print("Cantidad de capas tematicas: "+str(total_capas))
fecha_inicio = datetime.now()

for i in range(total_capas):
    capa = wfs.GetLayerByIndex(i)
    nombre_capa = capa.GetName()
    driver_shapefile = ogr.GetDriverByName('ESRI Shapefile')
    nombre_shp = nombre_capa + '.shp'
    ruta_descarga_shp = os.path.join(ruta_descarga, nombre_shp)
    data_source = driver_shapefile.CreateDataSource(ruta_descarga_shp)
    proyeccion = capa.GetSpatialRef()
    
    if tipo_geometria == 'point':
        geom = ogr.wkbPoint
    elif tipo_geometria == 'line':
        geom = ogr.wkbLineString
    elif tipo_geometria == 'polygon':
        geom = ogr.wkbPolygon
    nueva_capa = data_source.CreateLayer(nombre_capa, proyeccion, geom)
    propiedades_capa = capa.GetLayerDefn()
    total_columnas = propiedades_capa.GetFieldCount()
    print("Total de Columnas: "+ str(total_columnas))
    for columnas in range(total_columnas):
        nombre_columna = propiedades_capa.GetFieldDefn(columnas).GetName()
        if nombre_columna in ('SHAPE.STArea__', 'SHAPE.STLength__'):
            continue
        nueva_capa.CreateField(propiedades_capa.GetFieldDefn(columnas))

    for fila in capa:
    	nueva_capa.CreateFeature(fila)
    	print("Insertando FID: "+str(fila.GetFID()))

    print("Total de registros:"+ str(len(capa)))
    
print("URL: "+ url_wfs)
print("Fecha de inicio: "+ str(fecha_inicio))
fecha_fin = datetime.now()
print("Fecha fin: "+ str(fecha_fin))
print("Finalizado")       
