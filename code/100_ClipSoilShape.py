##Clip Raster Dataset by known extent - Left Bottom Right Top
import os
import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True ## 1
arcpy.env.workspace = 'C:/data/lokala_exe/Workspace/' #use m.2 drive as workspace to reduce processing time
arcpy.env.parallelProcessingFactor = '100%'
#Set global variables
LIDARSQUARES = 'C:/data/lokala_exe/Workspace/'
CLIPPED_SOIL = 'D:/WilliamLidberg/FeatureExtraction/Soil/splitsoilshape/' #path to output folder were clipped soilmap will be saved
RASTER_SOIL = 'D:/WilliamLidberg/FeatureExtraction/Soil/SplitSoilRaster/' #path to output folder were clipped rasters will be saved

#Loop to find all shapefiles in a folder and clip based on their extent
for file in os.listdir(LIDARSQUARES):
    if file.endswith('.shp'):

        #get extent of polygon file to clip raster
        desc = arcpy.Describe(file)
        clippextent = str(desc.extent)
        
        #local variables for clipping
        in_shape = 'D:/WilliamLidberg/jordartskartan_swe/jordartskarta_process.shp' #soil map to be clipped
        lidarsquare = LIDARSQUARES + file
        out_shape = CLIPPED_SOIL + file #The name of the input shapefile will be used to name the output file
        xy_tolerance = ""


        
        #local variables for Convert feature to raster
        in_feature = CLIPPED_SOIL + file
        out_raster = RASTER_SOIL + file.replace('.shp','.tif')
        cellSize = 2
        field = "JG2"
        
        #This is where the loop try to do the clipping for each file in the folder
        try:
            print('Running for file = ' + file)
            # Execute Clip
            arcpy.Clip_analysis(in_shape, lidarsquare, out_shape, xy_tolerance)
            # Execute FeatureToRaster
            arcpy.FeatureToRaster_conversion(in_feature, field, out_raster, cellSize)
            
        except:
            print("Error, you are doing it wrong!")
