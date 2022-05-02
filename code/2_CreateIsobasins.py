#The 2m DEm was resampled to a 50m DEM in the previous script and will now be used to create isobasins.

#First the DEM needs to be imported to Whitebox GAT.
wd = "D:/WilliamLidberg/FeatureExtraction/Isobasins/"
inputFiles = wd + "h50x50.tif" 
args = [inputFiles]
pluginHost.runPlugin("ImportGeoTiff", args, False)

#We need to pre-process the DEM by Breaching Depressions
BreachInput = "D:/WilliamLidberg/FeatureExtraction/Isobasins/h50x50.dep"
BreachOutput = "D:/WilliamLidberg/FeatureExtraction/Isobasins/NH50m_breached.dep"
maxBreachLength = "not specified"
outputPointer = "false"
performFlowAccumulation = "false"
Breachargs = [BreachInput, BreachOutput, maxBreachLength, outputPointer, performFlowAccumulation]
pluginHost.runPlugin("FastBreachDepressions", Breachargs, True)

#D8 flow pointer
demfile = "D:/WilliamLidberg/FeatureExtraction/Isobasins/NH50m_breached.dep"
pointerFile = "D:/WilliamLidberg/FeatureExtraction/Isobasins/D8_Pointer.dep"
runParallel = "true"
pointerargs = [demfile, pointerFile]
pluginHost.runPlugin("FlowPointerD8", pointerargs, False)

#D8 flow accumulation
pointerFile = "D:/WilliamLidberg/FeatureExtraction/Isobasins/D8_Pointer.dep"
FlowaccOutput = "D:/WilliamLidberg/FeatureExtraction/Isobasins/D8_ACC.dep"
outputType = "number of upslope grid cells"
logTransformOutput = "false"
args = [pointerFile, FlowaccOutput, outputType, logTransformOutput]
pluginHost.runPlugin("FlowAccumD8", args, False)


#Next we will use the flow pointer and flow accumulation to create three different sized of isobasins. This is done since the large basins don't go all the way to the coast. 
#Isobasins 10000
pointerFile = "D:/WilliamLidberg/FeatureExtraction/Isobasins/D8_Pointer.dep"
caFile = "D:/WilliamLidberg/FeatureExtraction/Isobasins/D8_ACC.dep"
Isobasin10000 = "D:/WilliamLidberg/FeatureExtraction/Isobasins/Isobasins10000.dep"
targetBasinSize1 = "10000"
args10000 = [pointerFile, caFile, Isobasin10000, targetBasinSize1]
pluginHost.runPlugin("Isobasin", args10000, False)
#Convert isobasins to polygons
outputFileC10000 = "D:/WilliamLidberg/FeatureExtraction/Isobasins/Isobasins10000.shp"
Cargs10000 = [Isobasin10000, outputFileC10000]
pluginHost.runPlugin("RasterToVectorPolygons", Cargs10000, False)

#Isobasins 100000
pointerFile = "D:/WilliamLidberg/FeatureExtraction/Isobasins/D8_Pointer.dep"
caFile = "D:/WilliamLidberg/FeatureExtraction/Isobasins/D8_ACC.dep"
Isobasin100000 = "D:/WilliamLidberg/FeatureExtraction/Isobasins/Isobasins100000.dep"
targetBasinSize2 = "100000"
args100000 = [pointerFile, caFile, Isobasin100000, targetBasinSize2]
pluginHost.runPlugin("Isobasin", args100000, False)
#Convert isobasins100000 to polygons
outputFileC100000 = "D:/WilliamLidberg/FeatureExtraction/Isobasins/Isobasins100000.shp"
Cargs100000 = [Isobasin100000, outputFileC100000]
pluginHost.runPlugin("RasterToVectorPolygons", Cargs100000, False)

#Isobasins 1000
Isobasin1000 = "D:/WilliamLidberg/FeatureExtraction/Isobasins/Isobasins1000.dep"
targetBasinSize3 = "1000"
args1000 = [pointerFile, caFile, Isobasin1000, targetBasinSize3]
pluginHost.runPlugin("Isobasin", args1000, False)
#Convert isobasins1000 to polygons
outputFileC1000 = "D:/WilliamLidberg/FeatureExtraction/Isobasins/Isobasins1000.shp"
Cargs1000 = [Isobasin1000, outputFileC1000]
pluginHost.runPlugin("RasterToVectorPolygons", Cargs1000, False)

#These isobasins are combined in arcgis pro
