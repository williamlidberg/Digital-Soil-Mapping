#This is the first script. It takes the 10m NMD data and resamples it to 2m.
from __future__ import print_function
import arcpy
from arcpy import env
import os
import sys
env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = '100%'
arcpy.env.compression = 'NONE' 

#Resample DEM
print('Resampling NMD')
arcpy.env.workspace = 'D:/WilliamLidberg/Data/GIS/NMD2018_basskikt_ogeneraliserad_Sverige_v1_0/'
arcpy.Resample_management('D:/WilliamLidberg/Data/GIS/NMD2018_basskikt_ogeneraliserad_Sverige_v1_0/NMDclipped.tif', 'D:/WilliamLidberg/FeatureExtraction/NMD2m/NDMResample2m.tif', '2', 'NEAREST')
print('Resampling complete')
