#By William Lidberg William.lidberg@slu.se
#The large isobasins don't cover all of Sweden so this script will clip and merge three sizes of isobasins. 
#The isobasins will then be used to clip features from the Swedish property map and the swedish 2m DEM.

# Import system modules
import arcpy, os
from arcpy import env
env.overwriteOutput = True
arcpy.env.parallelProcessingFactor = '100%'
# Set workspace
env.workspace = 'D:/WilliamLidberg/NH/Isobasins'
arcpy.env.compression = 'NONE'

#Isobasins created in whitebox GAT
LargeBasins = 'D:/WilliamLidberg/FeatureExtraction/Isobasins/Isobasins100000.shp'
MediumBasins = 'D:/WilliamLidberg/FeatureExtraction/Isobasins/Isobasins10000.shp'
SmallBasins = 'D:/WilliamLidberg/FeatureExtraction/Isobasins/Isobasins1000.shp'
#Erase outputs
eraseOutput1 = 'D:/WilliamLidberg/FeatureExtraction/Isobasins/EraseBigFromMedium.shp'
eraseOutput2 = 'D:/WilliamLidberg/FeatureExtraction/Isobasins/EraseMediumFromSmall.shp'
#Merged Isobasins
MergedIsobasins = 'D:/WilliamLidberg/FeatureExtraction/Isobasins/MergedIsobasins.shp'
xyTol = "1 Meters"

print ('Erasing overlapping isobasins')
arcpy.Erase_analysis(MediumBasins, LargeBasins, eraseOutput1, xyTol)
arcpy.Erase_analysis(SmallBasins, MediumBasins, eraseOutput2, xyTol)
print ('Erase complete')

# Merge
print ('Merge remaining isobasins')
arcpy.Merge_management([eraseOutput1, eraseOutput2, LargeBasins], MergedIsobasins)
print ('Merge complete')

#A text field with IDs are required to split the file
fieldLength = 10
print ('Adding new text filed to isobasin shapefile')
arcpy.AddField_management(MergedIsobasins, 'splitid', 'TEXT', field_length=fieldLength)
print ('Field added')

#We will simply copy the field ID to the split ID field.
print ('Calculate field')
arcpy.CalculateField_management(MergedIsobasins, "splitid", "!FID!", "PYTHON3", None)
print ('Field calculated')

#The split id field is used to split the isobasins to create one shapefile per basin.
featuretobesplit = MergedIsobasins
splitFeatures = MergedIsobasins
splitField = 'splitid'
outWorkspace = 'D:/WilliamLidberg/FeatureExtraction/SplittedFeatures/SplitIsobasins/'
clusterTol = "1 Meters"
print ('Splitting isobasin shapefile')
arcpy.Split_analysis(featuretobesplit, splitFeatures, splitField, outWorkspace, clusterTol)
print ('Splitting complete')

#Buffer splited isobasins with 1 km to avoid potential edge effects
SplittedBasin = 'D:/WilliamLidberg/FeatureExtraction/SplittedFeatures/SplitIsobasins/'
BufferedBasin = 'D:/WilliamLidberg/FeatureExtraction/SplittedFeatures/BufferedBasins/'
Distance = '1000 meter'
arcpy.env.workspace = 'D:/WilliamLidberg/FeatureExtraction/SplittedFeatures/SplitIsobasins'
# List the feature classes in the folder with splited isobasins
fcList = arcpy.ListFeatureClasses()

#River and lake polygons will be converted to raster at a later stage. That requires a field with a value.
#Add empy field named value.
Lakepolygons = 'D:/WilliamLidberg/Data/GIS/Fastighetskartan_vektor/riks/riks/water.shp'
print ('Adding new numeric field to River/Lake shapefile')
arcpy.AddField_management(Lakepolygons, 'value', 'DOUBLE')
print ('Field added')

#We will add the number 1 to the value field
print ('Add value to the new field')
arcpy.CalculateField_management(Lakepolygons, "value", "1", "PYTHON3", None)
print ('Value added calculated')

print ('Buffer splitted shapefiles by 1000 m') 
# Loop through the list and buffer all basins with 1000 meter
for inputFilename in os.listdir(SplittedBasin) :  
    if inputFilename.endswith('.shp') :  
        inputPath = os.path.join(SplittedBasin, inputFilename)  
        BufferoutputPath = os.path.join(BufferedBasin, inputFilename)  
        
	#Buffer
        arcpy.Buffer_analysis(inputPath, BufferoutputPath, Distance)  
print ('Buffering complete')

#Roads and railroads will be breached in whitebox but first they need to be merged.
#Shapefiles with all Swedish roads and railroads
Roads = 'D:/WilliamLidberg/Data/GIS/Fastighetskartan_vektor/riks/riks/vl_riks.shp'
RailRoads = 'D:/WilliamLidberg/Data/GIS/Fastighetskartan_vektor/riks/riks/jl_riks.shp'
MergedRoadsRailroads = 'D:/WilliamLidberg/Data/GIS/Fastighetskartan_vektor/riks/riks/MergeRoadsRailroads.shp'
print('Mering roads and railroads')
#Merge files
arcpy.Merge_management([Roads, RailRoads], MergedRoadsRailroads)
print('Merge complete')

#The buffered isobasins will be used to clip the roads, streams, rail roads and lakes.
#Input features
RoadsIn = 'D:/WilliamLidberg/Data/GIS/Fastighetskartan_vektor/riks/riks/MergeRoadsRailroads.shp'
StreamsIn = 'D:/WilliamLidberg/Data/GIS/Fastighetskartan_vektor/riks/riks/hl_riks.shp'

LakesIn = 'D:/WilliamLidberg/Data/GIS/Fastighetskartan_vektor/riks/riks/water.shp'
#Output folders
RoadsOut = 'D:/WilliamLidberg/FeatureExtraction/SplittedFeatures/SplitRoads/'
StreamsOut = 'D:/WilliamLidberg/FeatureExtraction/SplittedFeatures/SplitStreams/'
LakesOut = 'D:/WilliamLidberg/FeatureExtraction/SplittedFeatures/SplitLakes/'
xy_tolerance = ""

print ('Clipping roads, streams, railroads and water with buffered isobasins') 
for inputFilename in os.listdir(BufferedBasin) :  
    if inputFilename.endswith('.shp') :  
        #Set output locations
        BufferoutputPath = os.path.join(BufferedBasin, inputFilename)
        outputPathRoads = os.path.join(RoadsOut, inputFilename)
        outputPathStreams = os.path.join(StreamsOut, inputFilename)
        outputPathLakes = os.path.join(LakesOut, inputFilename)
        
	#Perform Clip
        arcpy.Clip_analysis(RoadsIn, BufferoutputPath, outputPathRoads, xy_tolerance)
        arcpy.Clip_analysis(StreamsIn, BufferoutputPath, outputPathStreams, xy_tolerance)	
        arcpy.Clip_analysis(LakesIn, BufferoutputPath, outputPathLakes, xy_tolerance)
  
print ('Clip Complete.')

#The buffered isobasins will also be used to clipp the swedish 2m DM
Swedish2mDEM = 'D:/WilliamLidberg/NH/h2x2_2x2.tif'
ClippedDEMfiles = 'D:/WilliamLidberg/FeatureExtraction/SplittedDEM/Raster/'
BufferedBasin = 'D:/WilliamLidberg/FeatureExtraction/SplittedFeatures/BufferedBasins/'

print ('Clip 2 m DEM with buffered isobasins') 
for inputFilename in os.listdir(BufferedBasin) :  
    if inputFilename.endswith('.shp') :
        #Set paths
        BufferPath = os.path.join(BufferedBasin, inputFilename)
        RasteroutputPath = os.path.join(ClippedDEMfiles, inputFilename.replace('.shp','.tif'))
        #Clip raster with buffered isobasins
        print ('Clipping isobasin nr ' + inputFilename.replace('.shp', ''))
        arcpy.Clip_management('D:/WilliamLidberg/NH/h2x2_2x2.tif', "#", RasteroutputPath, BufferPath, '0 ', 'ClippingGeometry')
print ('DEM clipped')
print ('Script is complete. Whitebox GAT will be used for the next part.')
#End of script. The next step is to import the DEMs into whitebox GAT and burn streams across roads.        

