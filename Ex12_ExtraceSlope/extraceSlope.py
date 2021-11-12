import arcpy,os
raster=arcpy.GetParameterAsText(0)
vector=arcpy.GetParameterAsText(1)
arcpy.AddMessage(vector)
reclassmap=arcpy.sa.RemapRange([[0,13,1],[13,25,2],[25,36,3],[36,48,4],[48,74,5],[74,90,6]])#分类级别
tempPath=os.environ["TMP"]#获取windows的临时目录
outslope=arcpy.sa.Slope(raster)
arcpy.AddMessage("坡度生成！")
#outslope.save(os.path.join(os.environ["TMP"],"f2"))

outReclassRR = arcpy.sa.Reclassify(outslope, "VALUE", reclassmap)
arcpy.AddMessage("重分类完成！")
#if arcpy.Exists(os.path.join(os.environ["TMP"],"slopelevel")):
#    arcpy.Delete_management(os.path.join(os.environ["TMP"],"slopelevel"))
#outReclassRR.save(os.path.join(os.environ["TMP"],"slopelevel"))
#arcpy.RasterToPolygon_conversion(os.path.join(os.environ["TMP"],"slopelevel"),os.path.join(os.environ["TMP"],"vectorpolygon"),"NO_SIMPLIFY","VALUE")

arcpy.RasterToPolygon_conversion(outReclassRR,vector,"NO_SIMPLIFY","VALUE")
arcpy.AddMessage("转换成矢量数据完成！")
arcpy.AddField_management(vector,"AREA","DOUBLE")
arcpy.AddMessage("添加AREA字段")
arcpy.CalculateField_management(vector,"AREA","!shape.area!","PYTHON_9.3")
arcpy.AddMessage("为AREA字段添加面积值完成")
arcpy.AddMessage("执行成功！")

#arcpy.MakeFeatureLayer_management(os.path.join(os.environ["TMP"],"vectorpolygon.shp"),"polygonLayer")
#arcpy.SelectLayerByAttribute_management("polygonLayer","NEW_SELECTION",'"Shape_Area"<=900')
#arcpy.Eliminate_management("polygonLayer",vector,"LENGTH","")
#arcpy.AddMessage(vector)