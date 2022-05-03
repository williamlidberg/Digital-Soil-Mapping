#Script by William Lidberg
print('Start Script')
import os
import arcpy
from os import path
arcpy.env.parallelProcessingFactor = "100%"
arcpy.env.pyramid = 'NONE' 
arcpy.env.compression = 'NONE'
arcpy.env.overwriteOutput = True
import arcpy, time
#sr = arcpy.SpatialReference(3006) # Swereff 99 TM
arcpy.CheckOutExtension("Spatial")


#set workspace to where your lidar suqares are saved
workspace = 'D:/WilliamLidberg/LiDAR_Rutor_Subset/'

#Set path and name of your selected squares
inputsquares = r'D:\WilliamLidberg\LiDAR_Rutor_Subset\Testomraden.shp'
splitFeatures = r'D:\WilliamLidberg\LiDAR_Rutor_Subset\Testomraden.shp' #yes, we are splitting the squares with the squares.

#set output folder and make sure it is empty.
splitoutput = 'D:/WilliamLidberg/CustomPrediction/splitlidarsquares/'     

splitField = "splitid"
arcpy.Split_analysis(inputsquares, splitFeatures, splitField, splitoutput)
print('splitting' + inputsquares)
## Copy composite rasters to new folder
OriginalDEMS = 'C:/data/lokala_exe/DEM/'
copyrasterDEMs = 'C:/data/lokala_exe/DEMO_DEM/'


#Loop for copying raster composites from the splitoutput list to the custom prediction folder.
for file in os.listdir(splitoutput):
    if file.endswith('.shp'):
         inputrasters = OriginalDEMS + file.replace('.shp', '.tif')
         outRaster = copyrasterDEMs + file.replace('.shp', '.tif')
         arcpy.CopyRaster_management(inputrasters,outRaster)
         
print('done')
