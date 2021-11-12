import arcpy,os,uuid
raster=arcpy.GetParameterAsText(0)
vector=arcpy.GetParameterAsText(1)
reclassmap=arcpy.sa.RemapRange([[0,13,1],[13,25,2],[25,36,3],[36,48,4],[48,74,5],[74,90,6]])#分类级别
tempPath=os.environ["TMP"]#获取windows的临时目录
outslope=arcpy.sa.Slope(raster)
#outslope.save(os.path.join(os.environ["TMP"],"f2"))
arcpy.AddMessage(tempPath)
outReclassRR = arcpy.sa.Reclassify(outslope, "VALUE", reclassmap)
#if arcpy.Exists(os.path.join(os.environ["TMP"],"slopelevel")):
#    arcpy.Delete_management(os.path.join(os.environ["TMP"],"slopelevel"))
#outReclassRR.save(os.path.join(os.environ["TMP"],"slopelevel"))
#arcpy.RasterToPolygon_conversion(os.path.join(os.environ["TMP"],"slopelevel"),os.path.join(os.environ["TMP"],"vectorpolygon"),"NO_SIMPLIFY","VALUE")


if arcpy.Exists(os.path.join(os.environ["TMP"],"vectorpolygon.shp")):
    arcpy.Delete_management(os.path.join(os.environ["TMP"],"vectorpolygon.shp"))
    arcpy.AddMessage(os.path.join(os.environ["TMP"],"vectorpolygon.shp"))
arcpy.RasterToPolygon_conversion(outReclassRR,os.path.join(os.environ["TMP"],"vectorpolygon.shp"),"NO_SIMPLIFY","VALUE")
arcpy.AddField_management(os.path.join(os.environ["TMP"],"vectorpolygon.shp"),"AREA","DOUBLE")
arcpy.CalculateField_management(os.path.join(os.environ["TMP"],"vectorpolygon.shp"),"AREA","!shape.area!","PYTHON_9.3")


#arcpy.MakeFeatureLayer_management(os.path.join(os.environ["TMP"],"vectorpolygon.shp"),"polygonLayer")
#arcpy.SelectLayerByAttribute_management("polygonLayer","NEW_SELECTION",'"Shape_Area"<=900')
#arcpy.Eliminate_management("polygonLayer",vector,"LENGTH","")
#arcpy.AddMessage(vector)