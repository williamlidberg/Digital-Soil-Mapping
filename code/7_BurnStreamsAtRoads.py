#This script will burn streams from theproperty map across roads from the property map.
#Now when the DEMs, streams and roads are all split into isobasins we can use parallel processing to greatly reduce processing time.
#Name of tool to run
pluginName = 'BurnStreamsAtRoads'
#Define location and name of textfile containing the arguments for BurnStreamsAtRoads
parameterFile = 'C:/data/lokala_exe/Python/WhiteboxTools/Arguments_BurnStreamsAtRoads.txt'
#Supress returns means that we will not load all files into the display windows of whitebox GAT.
suppressReturns = 'true'
args = [pluginName, parameterFile, suppressReturns]
pluginHost.runPlugin("RunPluginInParallel", args, True)
