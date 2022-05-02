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
FilledDEMs = 'D:\\WilliamLidberg\\FeatureExtraction\\FillNoData\\'
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
        global FilledDEMs


        wbt = WhiteboxTools()
        wbt.set_whitebox_dir(wb_dir)

        #orginal self.files
        originaldems = DEMS + self.file

        #Missing data filled
        filled = FilledDEMs + self.file

        args1 = ['--input="' + originaldems + '"', '--output="' + filled + '"', '--filter="' + '100' + '"', '--weight="' + '2' + '"']


        try:
            wbt.run_tool('FillMissingData', args1, callback)

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
