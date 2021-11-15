import arcpy


fc=".\data\data.gdb\polyline"
cursor=arcpy.da.SearchCursor(fc,["id","OID@","SHAPE@"])
for row in cursor:
	print ("Feature {0}".format(row[1]))
	for point in row[2].getPart(0):
		print ("{0},{1}".format(point.X,point.Y))
