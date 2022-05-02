#This script is based on code by John Lindsey and Kim Lindgren and has been modified by William Lidberg.
#!/usr/bin/env python3
from __future__ import print_function
import threading
import time
import os
import sys
from whitebox_tools import WhiteboxTools
wb_dir = os.path.dirname('C:\\data\\lokala_exe\\Python\\WhiteboxTools\\')

#Local variables
DEMS = 'D:\\WilliamLidberg\\FeatureExtraction\\BurnStreamsAtRoads\\'
RASTERSTREAMS_1ha = 'D:\\WilliamLidberg\\FeatureExtraction\\rasterstreams\\1ha\\'
RASTERSTREAMS_5ha = 'D:\\WilliamLidberg\\FeatureExtraction\\rasterstreams\\5ha\\'
RASTERSTREAMS_10ha = 'D:\\WilliamLidberg\\FeatureExtraction\\rasterstreams\\10ha\\'
RASTERSTREAMS_20ha = 'D:\\WilliamLidberg\\FeatureExtraction\\rasterstreams\\20ha\\'
POLYGONLAKES = 'D:\\WilliamLidberg\\FeatureExtraction\\SplittedFeatures\\SplitLakes\\'
RASTERLAKES = 'D:\\WilliamLidberg\\FeatureExtraction\\SplittedFeatures\\RasterLakesRivers\\'
COMBINED_1ha = 'D:\\WilliamLidberg\\FeatureExtraction\\SplittedFeatures\\CombinedLakesAndRivers\\1ha\\'
COMBINED_5ha = 'D:\\WilliamLidberg\\FeatureExtraction\\SplittedFeatures\\CombinedLakesAndRivers\\5ha\\'
COMBINED_10ha = 'D:\\WilliamLidberg\\FeatureExtraction\\SplittedFeatures\\CombinedLakesAndRivers\\10ha\\'
COMBINED_20ha = 'D:\\WilliamLidberg\\FeatureExtraction\\SplittedFeatures\\CombinedLakesAndRivers\\20ha\\'

#Set number of threads to use. The SGU computer has 10 cores and 20 threads. 
maxThreads = 19      #Change this to adjust the number of cores used
activeThreads = 0    #Don't touch this


def callback(out_str):
    ''' Create a custom callback to process the text coming out of the tool.
    If a callback is not provided, it will simply print the output stream.
    A custom callback allows for processing of the output stream.
    '''
    try:
        if not hasattr(callback, 'prev_line_progress'):
            callback.prev_line_progress = False
        if "%" in out_str:
            str_array = out_str.split(" ")
            label = out_str.replace(str_array[len(str_array) - 1], "").strip()
            progress = int(
                str_array[len(str_array) - 1].replace("%", "").strip())
            if callback.prev_line_progress:
                print('{0} {1}%'.format(label, progress), end="\r")
            else:
                callback.prev_line_progress = True
                print(out_str)
        elif "error" in out_str.lower():
            print("ERROR: {}".format(out_str))
            callback.prev_line_progress = False
        elif "elapsed time (excluding i/o):" in out_str.lower():
            elapsed_time = ''.join(
                ele for ele in out_str if ele.isdigit() or ele == '.')
            units = out_str.lower().replace("elapsed time (excluding i/o):",
                                            "").replace(elapsed_time, "").strip()
            print("Elapsed time: {0}{1}".format(elapsed_time, units))
            callback.prev_line_progress = False
        else:
            if callback.prev_line_progress:
                print('\n{0}'.format(out_str))
                callback.prev_line_progress = False
            else:
                print(out_str)

    except:
        print(out_str)
class workerThread(threading.Thread):
    def __init__(self, indata):
        threading.Thread.__init__(self)
        self.file = indata

    def run(self):
        global activeThreads
        activeThreads += 1

        #################################
        ##### Begin here #####
        #################################
        #Set Global variables
        global wb_dir
        global DEMS
        global RASTERSTREAMS_1ha
        global RASTERSTREAMS_5ha
        global RASTERSTREAMS_10ha
        global RASTERSTREAMS_20ha
        global POLYGONLAKES
        global RASTERLAKES
        global COMBINED_1ha
        global COMBINED_5ha
        global COMBINED_10ha
        global COMBINED_20ha

        wbt = WhiteboxTools()
        wbt.set_whitebox_dir(wb_dir)


        #orginal self.files
        originaldems = DEMS + self.file

        #Convert water polygons from the property map to raster
        waterpolygons = POLYGONLAKES + self.file.replace('.dep', '.shp')
        rasterlakes = RASTERLAKES + self.file
        basefile = DEMS + self.file
        fieldname = "value"
        nodata = False
        base = DEMS + self.file
        cellsize = None
        args1 = ['--input="' + rasterlakes + '"', '--field="' + fieldname + '"', '--output="' + rasterlakes + '"', '--nodata="' + nodata + '"', '--cell_size="' + cellsize + '"', '--base="' + base + '"'] 

        #Merge raster streams with raster lakes
        #All stream networks will be merged with the same lake/river rasters
        rasterlakes =  RASTERLAKES + self.file
        #Each stream network needs to be specified
        rasterstream1ha = RASTERSTREAMS_1ha + self.file
        rasterstream5ha = RASTERSTREAMS_5ha + self.file
        rasterstream10ha = RASTERSTREAMS_10ha + self.file
        rasterstream20ha = RASTERSTREAMS_20ha + self.file
        #same for stream network output
        merged1ha = COMBINED_1ha + self.file
        merged5ha = COMBINED_5ha + self.file
        merged10ha = COMBINED_10ha + self.file
        merged20ha = COMBINED_20ha + self.file
        #one argument for each merger
        argsOr1ha = ['--input1="' + rasterstream1ha + '"', '--input2="' + rasterlakes + '"', '--output="' + merged1ha + '"']  
        argsOr5ha = ['--input1="' + rasterstream5ha + '"', '--input2="' + rasterlakes + '"', '--output="' + merged5ha + '"']
        argsOr10ha = ['--input1="' + rasterstream10ha + '"', '--input2="' + rasterlakes + '"', '--output="' + merged10ha + '"']
        argsOr20ha = ['--input1="' + rasterstream20ha + '"', '--input2="' + rasterlakes + '"', '--output="' + merged20ha + '"'] 
        
        try:
            wbt.run_tool('VectorPolygonsToRaster', args1, callback)
            wbt.run_tool('Or', argsOr1ha, callback)
            wbt.run_tool('Or', argsOr5ha, callback)
            wbt.run_tool('Or', argsOr10ha, callback)
            wbt.run_tool('Or', argsOr20ha, callback)
        except:
            print('Unexpected error:', sys.exc_info()[0])
            raise
        #################################
        ##### End here #####
        #################################

        activeThreads -= 1

for inputfile in os.listdir(DEMS):
    if inputfile.endswith('.tif'):
        worker = workerThread(inputfile).start()

    while activeThreads >= maxThreads:
        pass
