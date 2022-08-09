aprx = arcpy.mp.ArcGISProject("CURRENT")
m = aprx.listMaps("Map")[0]

for lyr in m.listLayers("Subdivisions"):
    if lyr.supports("DEFINITIONQUERY"):
        desc = arcpy.Describe(lyr)
        fid_list = desc.FIDSet.split(";")
        query = '{} IN ({})'.format(desc.OIDFieldName, ",".join(fid_list))
        lyr.definitionQuery = query
