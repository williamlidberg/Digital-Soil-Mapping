##convert shape to raster
import os
import arcpy
from arcpy import env
arcpy.env.overwriteOutput = True ## 1
arcpy.env.workspace = 'C:/data/lokala_exe/Workspace/' #use m.2 drive as workspace to reduce processing time
arcpy.env.parallelProcessingFactor = '100%'
arcpy.env.compression = "NONE"
#Set global variables

CLIPPED_SOIL = 'D:/WilliamLidberg/FeatureExtraction/Soil/splitsoilshape/' #path to output folder were clipped soilmap will be saved
RASTER_SOIL = 'D:/WilliamLidberg/FeatureExtraction/Soil/SplitSoilRaster/' #path to output folder were clipped rasters will be saved

#Loop to find all shapefiles in a folder and clip based on their extent
for file in os.listdir(CLIPPED_SOIL):
    if file.endswith('.shp'):
       
        #local variables for Convert feature to raster
        in_feature = CLIPPED_SOIL + file
        out_raster = RASTER_SOIL + file.replace('.shp','.tif')
        cellSize = 2
        field = "ProcessCod"
        
        #This is where the loop try to do the clipping for each file in the folder
        try:
            print('Running for file = ' + file)
            # Execute FeatureToRaster
            arcpy.FeatureToRaster_conversion(in_feature, field, out_raster, cellSize)
            
        except:
            print("Error, you are doing it wrong!")
