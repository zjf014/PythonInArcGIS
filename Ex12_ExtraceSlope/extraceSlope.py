import arcpy,os
raster=arcpy.GetParameterAsText(0)
vector=arcpy.GetParameterAsText(1)
arcpy.AddMessage(vector)
reclassmap=arcpy.sa.RemapRange([[0,13,1],[13,25,2],[25,36,3],[36,48,4],[48,74,5],[74,90,6]])#���༶��
tempPath=os.environ["TMP"]#��ȡwindows����ʱĿ¼
outslope=arcpy.sa.Slope(raster)
arcpy.AddMessage("�¶����ɣ�")
#outslope.save(os.path.join(os.environ["TMP"],"f2"))

outReclassRR = arcpy.sa.Reclassify(outslope, "VALUE", reclassmap)
arcpy.AddMessage("�ط�����ɣ�")
#if arcpy.Exists(os.path.join(os.environ["TMP"],"slopelevel")):
#    arcpy.Delete_management(os.path.join(os.environ["TMP"],"slopelevel"))
#outReclassRR.save(os.path.join(os.environ["TMP"],"slopelevel"))
#arcpy.RasterToPolygon_conversion(os.path.join(os.environ["TMP"],"slopelevel"),os.path.join(os.environ["TMP"],"vectorpolygon"),"NO_SIMPLIFY","VALUE")

arcpy.RasterToPolygon_conversion(outReclassRR,vector,"NO_SIMPLIFY","VALUE")
arcpy.AddMessage("ת����ʸ��������ɣ�")
arcpy.AddField_management(vector,"AREA","DOUBLE")
arcpy.AddMessage("���AREA�ֶ�")
arcpy.CalculateField_management(vector,"AREA","!shape.area!","PYTHON_9.3")
arcpy.AddMessage("ΪAREA�ֶ�������ֵ���")
arcpy.AddMessage("ִ�гɹ���")

#arcpy.MakeFeatureLayer_management(os.path.join(os.environ["TMP"],"vectorpolygon.shp"),"polygonLayer")
#arcpy.SelectLayerByAttribute_management("polygonLayer","NEW_SELECTION",'"Shape_Area"<=900')
#arcpy.Eliminate_management("polygonLayer",vector,"LENGTH","")
#arcpy.AddMessage(vector)