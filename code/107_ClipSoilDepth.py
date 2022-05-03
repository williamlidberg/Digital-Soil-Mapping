##Clip Raster Dataset by known extent - Left Bottom Right Top
import os
import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True ## 1
arcpy.env.workspace = 'C:/data/lokala_exe/DEM/' #use SSD drive as workspace to reduce processing time
#Use all cores of the machine. 
arcpy.env.parallelProcessingFactor = '100'
arcpy.env.pyramid = 'NONE' 
arcpy.env.compression = 'NONE' 
#Set Local variables
LIDARSQUARES = 'C:/data/lokala_exe/DEM/' #Save clip files on SSD drive to reduce processing time
RASTERTOBECLIPPED = 'D:/WilliamLidberg/Data/GIS/SoilDepth/Jorddjup2m32bit.tif' #change this to the raster that shoud be clipped.
CLIPPED_RASTERS = 'D:/WilliamLidberg/FeatureExtraction/Completed_Features/SoilDepth/' #path to output folder were clipped rasters will be saved

#Loop to find all rasters in a folder and clip based on their extent
for file in os.listdir(LIDARSQUARES):
    if file.endswith('.tif'):
        #local variables
        out_raster = CLIPPED_RASTERS + file #The name of the input shapefile will be used to name the output raster
        in_raster = 'D:/WilliamLidberg/Data/GIS/SoilDepth/Jorddjup2m32bit.tif' #Raster mosaic to be clipped
        in_template_dataset = LIDARSQUARES + file #use DEM for all other tools
        #get extent of file to clip raster
        desc = arcpy.Describe(file)
        clippextent = str(desc.extent)


        try:
            print('Running for file = ' + file)
            arcpy.management.Clip(in_raster, clippextent, out_raster, in_template_dataset, "#", "#", "MAINTAIN_EXTENT")
        except:
            print("Error, you are doing it wrong!")
