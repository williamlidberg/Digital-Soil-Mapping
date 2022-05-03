#This is the first script. It takes the 2m DEM and resamples it to a 50 m DEM
#The 50m DEM will be used to create isobasins in whitebox GAT.
from __future__ import print_function
import arcpy
from arcpy import env
import os
import sys
env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = '100%'
arcpy.env.compression = 'NONE' #Whitebox can't read compressed files.

#Resample DEM
print('Resampling DEM')
arcpy.env.workspace = 'D:/WilliamLidberg/Data/GIS/NH/'
arcpy.Resample_management('D:/WilliamLidberg/Data/GIS/NH/h2x2_2x2.tif', 'D:/WilliamLidberg/FeatureExtraction/Isobasins/h50x50.tif', '50', 'NEAREST')
print('Resampling complete')
