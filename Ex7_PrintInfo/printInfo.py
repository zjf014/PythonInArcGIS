# -*- coding: utf-8 -*-

import arcpy


layerString = ".\HSSymbols.lyr"
#layerString = "D:\Code\Python\ArcPy\Ex7_PrintInfo\HSSymbols.lyr"
desc = arcpy.Describe(layerString)

# Print selected layer and describe object properties
# 
print("Name: {}".format(desc.name))
if hasattr(desc, "layer"):
    print("Layer name: {}".format(desc.layer.name))
    print("Layer data source: {}".format(desc.layer.catalogPath))
    print(".lyr file: {}".format(desc.catalogPath))
else:
    print("Layer name: {}".format(desc.name))
    print("Layer data source: {}".format(desc.catalogPath))

if desc.FIDSet != '':
    print("Number of selected features: {}".format(len(desc.FIDSet.split(";"))))
