#We will specify the textfile where each row contains the arguments to this tool.

#Import GeoTIFFs
pluginName = 'ImportGeoTiff'
#Define location and name of textfile containing the arguments for importGeotiff
parameterFile = 'C:/data/lokala_exe/Python/WhiteboxTools/listofrasterstoimport.txt'
#Supress returns means that we will not load all files into the display windows of whitebox GAT.
suppressReturns = 'true'
args = [pluginName, parameterFile, suppressReturns]
pluginHost.runPlugin("RunPluginInParallel", args, True)
print ('Import Geotiffs')

