import random
import numpy as np
import arcpy
import datetime
import os

starttime=datetime.datetime.now()
print("Start time:")
print(starttime)

f_path=r'C:\Data\2d_zones_id_txt.txt'
a=np.loadtxt(f_path)
for i in range(len(a)):
    for j in range(len(a[0])):
        if a[i][j]>0:
            a[i][j]=random.randint(0,100)

np.savetxt(r'C:\Data\a.txt',a,'%d')
print("TXT file is Done.")


f=open(r'C:\Data\test.txt','w')
f.writelines('ncols         1371')
f.write('\n')
f.writelines('nrows         1351')
f.write('\n')
f.writelines('xllcorner     423937.63417')
f.write('\n')
f.writelines('yllcorner     2881429.248249')
f.write('\n')
f.writelines('cellsize      10')
f.write('\n')
f.writelines('NODATA_value  -9999')
f.write('\n')
for line in open(r'C:\Data\a.txt','r'):
    f.writelines(line)

f.close()
print("ASCII file is Done.")

inASCII = r'C:\Data\test.txt'
outRaster = r'C:\Data\test.tif'
rasterType = "INTEGER"
arcpy.ASCIIToRaster_conversion(inASCII, outRaster, rasterType)
print("Raster file is Done.")

# createGISServerConnectionFile,define local variable
wrkpc = r"C:\Data"
out_folder_path = wrkpc
con_Filename = "test.ags"
server_url = r"http://localhost:6080/arcgis/admin"
staging_folder_path = wrkpc
username = "admin"
password = "admin"

arcpy.mapping.CreateGISServerConnectionFile("USE_GIS_SERVICES",
                                            out_folder_path,
                                            con_Filename,
                                            server_url,
                                            "ARCGIS_SERVER",
                                            False,
                                            staging_folder_path,
                                            username,
                                            password,
                                            "SAVE_USERNAME")
print("Connection file (.ags) is Done.")

# define local variables
mdpath = outRaster
con = os.path.join(wrkpc, con_Filename)
service = 'test_service'
sddraft = os.path.join(wrkpc, service+".sddraft")
sd = os.path.join(wrkpc, service+".sd")
print("Draft file (.sd) is Done.")

# creste service definition draft
analysis = arcpy.CreateImageSDDraft(mdpath,
                                            sddraft,
                                            service,
                                            "FROM_CONNECTION_FILE",
                                            con,
                                            False,
                                            "test",
                                            "","")

#stage and upload the service if the sddraft analysis didn't contain errors
if analysis['errors'] == {}:
    # excute StageService
    arcpy.StageService_server(sddraft,sd)
    # excute UploadServiceDfinition
    arcpy.UploadServiceDefinition_server(sd,con)
else:
    # if the sddraft analysis contained errors,display them
    print analysis['errors']


endtime=datetime.datetime.now()
print("Ending time:")
print(endtime)

print(endtime-starttime)
