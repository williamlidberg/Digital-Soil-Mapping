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
DEMS = 'D:\\WilliamLidberg\\FeatureExtraction\\CompleteBreached\\'
RASTERSTREAMS_1ha = 'D:\\WilliamLidberg\\FeatureExtraction\\rasterstreams\\1ha\\'
RASTERSTREAMS_5ha = 'D:\\WilliamLidberg\\FeatureExtraction\\rasterstreams\\5ha\\'
RASTERSTREAMS_10ha = 'D:\\WilliamLidberg\\FeatureExtraction\\rasterstreams\\10ha\\'
RASTERSTREAMS_20ha = 'D:\\WilliamLidberg\\FeatureExtraction\\rasterstreams\\20ha\\'

ELEVATIONABOVESTREAM_1ha = 'D:\\WilliamLidberg\\FeatureExtraction\\ElevationAboveStream\\EAS1ha\\'
ELEVATIONABOVESTREAM_5ha = 'D:\\WilliamLidberg\\FeatureExtraction\\ElevationAboveStream\\EAS5ha\\'
ELEVATIONABOVESTREAM_10ha = 'D:\\WilliamLidberg\\FeatureExtraction\\ElevationAboveStream\\EAS10ha\\'
ELEVATIONABOVESTREAM_20ha = 'D:\\WilliamLidberg\\FeatureExtraction\\ElevationAboveStream\\EAS20ha\\'

#Set number of threads to use. The SGU computer has 10 cores and 20 threads. 
maxThreads = 1      #Change this to adjust the number of cores used
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
        global ELEVATIONABOVESTREAM_1ha
        global ELEVATIONABOVESTREAM_5ha
        global ELEVATIONABOVESTREAM_10ha
        global ELEVATIONABOVESTREAM_20ha
        
        wbt = WhiteboxTools()
        wbt.set_whitebox_dir(wb_dir)

        #orginal self.files
        originaldems = DEMS + self.file

        
        #1ha
        Streams1ha = RASTERSTREAMS_1ha + self.file
        elevationabovestream1ha = ELEVATIONABOVESTREAM_1ha + self.file.replace('.dep', '.tif')
        #5ha
        Streams5ha = RASTERSTREAMS_5ha + self.file
        elevationabovestream5ha = ELEVATIONABOVESTREAM_5ha + self.file.replace('.dep', '.tif')
        #10ha
        Streams10ha = RASTERSTREAMS_10ha + self.file
        elevationabovestream10ha = ELEVATIONABOVESTREAM_10ha + self.file.replace('.dep', '.tif')
        #20ha
        Streams20ha = RASTERSTREAMS_20ha + self.file
        elevationabovestream20ha = ELEVATIONABOVESTREAM_20ha + self.file.replace('.dep', '.tif')


        #Arguments for Elevation above stream
        args1 = ['--dem="' + originaldems + '"',  '--streams="' + Streams1ha + '"', '--output="' + elevationabovestream1ha + '"']        
        args2 = ['--dem="' + originaldems + '"',  '--streams="' + Streams5ha + '"', '--output="' + elevationabovestream5ha + '"']
        args3 = ['--dem="' + originaldems + '"',  '--streams="' + Streams10ha + '"', '--output="' + elevationabovestream10ha + '"']
        args4 = ['--dem="' + originaldems + '"',  '--streams="' + Streams20ha + '"', '--output="' + elevationabovestream20ha + '"']
        
        
        try:
            wbt.run_tool('ElevationAboveStream', args1, callback)
            #wbt.run_tool('ElevationAboveStream', args2, callback)
            wbt.run_tool('ElevationAboveStream', args3, callback)
            #wbt.run_tool('ElevationAboveStream', args4, callback)
            

        except:
            print('Unexpected error:', sys.exc_info()[0])
            raise
        #################################
        ##### End here #####
        #################################

        activeThreads -= 1

for inputfile in os.listdir(DEMS):
    if inputfile.endswith('.dep'):
        worker = workerThread(inputfile).start()

    while activeThreads >= maxThreads:
        pass
