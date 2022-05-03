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
DEMS = 'D:\\WilliamLidberg\\FeatureExtraction\\FillNoData\\'
BREACHED = 'D:\\WilliamLidberg\\FeatureExtraction\\CompleteBreached\\'
POINTER = 'D:\\WilliamLidberg\\FeatureExtraction\\Pointer\\'
FLOWACC = 'D:\\WilliamLidberg\\FeatureExtraction\\flowacc\\'
RASTERSTREAMS_1ha = 'D:\\WilliamLidberg\\FeatureExtraction\\rasterstreams\\1ha\\'
RASTERSTREAMS_10ha = 'D:\\WilliamLidberg\\FeatureExtraction\\rasterstreams\\10ha\\'

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
        global BREACHED
        global POINTER
        global FLOWACC
        global RASTERSTREAMS_1ha
        global RASTERSTREAMS_10ha


        wbt = WhiteboxTools()
        wbt.set_whitebox_dir(wb_dir)

        #orginal self.files
        originaldems = DEMS + self.file

        #Breach
        breachout = BREACHED + self.file
        args1 = ['--input="' + originaldems + '"', '--output="' + breachout + '"']

        #Flowpopinter
        pointerout = POINTER + self.file
        args2 = ['--dem="' + breachout + '"', '--output="' + pointerout + '"']

        #Flowaccumulation from DEM (not from pointer)
        Flowaccout = FLOWACC + self.file
        args3 = ['--dem="' + breachout + '"', '--output="' + Flowaccout + '"', '--out_type="' + 'Cells"' + '"']

        #Extract raster streams for two different stream initation thresholds
        #1ha Stream network
        Streamsout1ha = RASTERSTREAMS_1ha + self.file
        args4 = ['--flow_accum="' + Flowaccout + '"',  '--output="' + Streamsout1ha + '"', '--threshold="' + '2500.0"' + '"', '--zero_background"']

        #10ha Stream network
        Streamsout10ha = RASTERSTREAMS_10ha + self.file
        args6 = ['--flow_accum="' + Flowaccout + '"',  '--output="' + Streamsout10ha + '"', '--threshold="' + '25000.0"' + '"', '--zero_background"']

        try:
            wbt.run_tool('BreachDepressions', args1, callback)
            wbt.run_tool('D8Pointer', args2, callback)
            wbt.run_tool('D8FlowAccumulation', args3, callback)
            wbt.run_tool('ExtractStreams', args4, callback)
            wbt.run_tool('ExtractStreams', args6, callback)

            

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
