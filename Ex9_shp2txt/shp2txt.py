# -*- coding: utf-8 -*-


import arcpy
from arcpy import env
import math

dpath="./"
#print(dpath.decode("utf-8"))
env.workspace=dpath

fc=arcpy.Describe("20190606.shp")
#print(fc.shapeType)

fl="20190606.shp"

cursor=arcpy.da.SearchCursor(fl,["MJ","DKBH","DKMC","TFH",'SHAPE@','SHAPE@AREA','TX'])
for row in cursor:
    
    dname=row[2]
    #print(dname.encode('gb2312'))
    darea=row[5]/10000
    did=row[1]
    dtfh=row[3]
    dtx=row[6]
    print(dname)
    print(darea)
    print(did)
    print(dtfh)
    print(dtx)
    #darea=row.getValue('MJ')
    #f=open(dpath.decode('utf-8')+"/"+dname+".txt","w+")
    f=open(dpath+dname+".txt","w+")

    #头文件
    #tem=open(dpath.decode('utf-8')+"/tmp.txt","r")
    tem=open(dpath+"tmp.txt","r")
    for l in tem.readlines():
        #print(l)
        f.write(l)

    tem.close()


    #点坐标
    partnum = 0
    for part in row[4]:

        #地块信息
        print("Part {}:".format(partnum))
        f.write("\n{},{},{},{},{},{},{},{},@".format(part.count,darea,did,dname.encode('gb2312'),dtx.encode('gb2312'),dtfh,"",""))
        #print(part.count)
        n=1
        #m=math.log(10,part.count-1)
        #print(m)

        for pnt in part:            
            if pnt:
                # Print x,y coordinates of current point
                #                
                n=1 if n==part.count else n
                fid="{}{}".format("J",n) if n>=10 else "{}{}".format("J0",n)

                print("{},{},{}".format(fid,pnt.Y, pnt.X))
                f.write("\n{},{},{},{}".format(fid,1,pnt.Y, pnt.X))
                n+=1
            else:
                # If pnt is None, this represents an interior ring
                #                
                print("Interior Ring:")
        partnum += 1
    #f.write("\n面")

    #关闭
    f.close()


print("done.")
