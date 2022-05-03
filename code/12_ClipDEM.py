##Clip Raster Dataset by known extent - Left Bottom Right Top
import os
import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True ## 1
arcpy.env.workspace = 'C:/data/lokala_exe/Workspace/' #use m.2 drive as workspace to reduce processing time
arcpy.env.parallelProcessingFactor = '100%'
#Set Local variables
LIDARSQUARES = 'C:/data/lokala_exe/Workspace/' #Save clip files on m.2 drive to reduce processing time
CLIPPED_RASTERS = 'D:/WilliamLidberg/FeatureExtraction/Completed_Features/DEM/' #path to output folder were clipped rasters will be saved
RASTERTOBECLIPPED = 'D:/WilliamLidberg/Data/GIS7NH/h2x2_2x2.tif'
#Loop to find all shapefiles in a folder and clip based on their extent
for file in os.listdir(LIDARSQUARES):
    if file.endswith('.shp'):
        #local variables
        out_raster = CLIPPED_RASTERS + file.replace('.shp', '.tif') #The name of the input shapefile will be used to name the output raster
        in_raster = 'Z:/WilliamLidberg/Data/GIS/NH/h2x2_2x2.tif' #Raster mosaic to be clipped
#        in_template_dataset = '' use DEM for all other tools. This will help with snapping

        #get extent of polygon file to clip raster
        desc = arcpy.Describe(file)
        clippextent = str(desc.extent)

        #This is where the loop try to do the clipping for each file in the folder
        try:
            print('Running for file = ' + file)
            arcpy.management.Clip(in_raster, clippextent, out_raster)
        except:
            print("Error, you are doing it wrong!")
