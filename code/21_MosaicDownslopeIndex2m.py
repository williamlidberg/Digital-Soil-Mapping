#Script by William Lidberg
print('Start Script')
import os
import arcpy
from arcpy import (CheckOutExtension, da)
from arcpy.management import MosaicToNewRaster
from os import path
arcpy.env.parallelProcessingFactor = "100%"
arcpy.env.pyramid = 'NONE' #Don't build pyramids

arcpy.env.compression = 'NONE' #Don't compress the data. Whitebox can't read compressed files.
import arcpy, time

workspace = r'D:\WilliamLidberg\FeatureExtraction\DownSlopeIndex'
sr = arcpy.SpatialReference(3006) # Swereff 99 TM
arcpy.CheckOutExtension("Spatial")

#Make list of rasters to mosaic
rasters = []
walk = arcpy.da.Walk(workspace, topdown=True, datatype="RasterDataset")
for dirpath, dirnames, filenames in da.Walk(workspace, topdown=True, datatype="RasterDataset"):
     for filename in filenames:
          rasters.append(filename)


ras_list = ';'.join(rasters)
#print('List of input raster files')
#print('')
print(ras_list)
#Its important that the mosaic method is set to MINIMUM for DTW and Elevation Above Stream. each file has a 1 km overlap. 
MosaicToNewRaster(rasters, r'D:\WilliamLidberg\FeatureExtraction\DownSlopeIndex2mMosaic', 'DI2m.tif', '', '32_BIT_FLOAT', '2', '1', 'MINIMUM')
print('Done with DI2m')

#EAS 10ha
workspace = r'D:\WilliamLidberg\FeatureExtraction\ElevationAboveStream\EAS10ha'
sr = arcpy.SpatialReference(3006) # Swereff 99 TM
arcpy.CheckOutExtension("Spatial")

#Make list of rasters to mosaic
rasters = []
walk = arcpy.da.Walk(workspace, topdown=True, datatype="RasterDataset")
for dirpath, dirnames, filenames in da.Walk(workspace, topdown=True, datatype="RasterDataset"):
     for filename in filenames:
          rasters.append(filename)


ras_list = ';'.join(rasters)
#print('List of input raster files')
#print('')
print(ras_list)
#Its important that the mosaic method is set to MINIMUM for DTW and Elevation Above Stream. each file has a 1 km overlap. 
MosaicToNewRaster(rasters, r'D:\WilliamLidberg\FeatureExtraction\ElevationAboveStream\EAS10haMosaic', 'EAS10ha.tif', '', '16_BIT_UNSIGNED', '2', '1', 'MINIMUM')
print('Done with 10ha EAS')
