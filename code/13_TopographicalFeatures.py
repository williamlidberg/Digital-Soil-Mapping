#!/usr/bin/env python3
#References: Grohmann, C. H., Smith, M. J., & Riccomini, C. (2010). Multiscale analysis of topographic surface roughness in the Midland Valley, Scotland. IEEE Transactions on Geoscience and Remote Sensing, 49(4), 1200-1213.
#Ko, M., Kang, H., ulrim Kim, J., Lee, Y., & Hwang, J. E. (2016, July). How to measure quality of affordable 3D printing: Cultivating quantitative index in the user community. In International Conference on Human-Computer Interaction (pp. 116-121). Springer, Cham.
#Lindsay, J. B., & Newman, D. R. (2018). Hyper-scale analysis of surface roughness. PeerJ Preprints, 6, e27110v1.
from __future__ import print_function
import threading
import time
import os
import sys

from whitebox_tools import WhiteboxTools

#This script was run at SLU and is based on the lidar tiles
wb_dir = os.path.dirname('D:/NILS2/WBT/')
DEM = 'D:/NILS2/DEMs/'
CVA = 'D:/NILS2/CircularVarianceOfAspect/' #Grohmann, C. H., Smith, M. J., & Riccomini, C. (2010). Multiscale analysis of topographic surface roughness in the Midland Valley, Scotland. IEEE Transactions on Geoscience and Remote Sensing, 49(4), 1200-1213.
RUGGED = 'D:/NILS2/RuggednessIndex/'
SDOS = 'D:/NILS2/StandardDeviationFromSlope/'
DFME = 'D:/NILS2/DeviationfromMeanElevation/'
FPS = 'D:/NILS2/FeaturePreservingSmoothing/'
EXTRACTVALLEYS = 'D:/NILS2/ExtractValleys/'
maxThreads = 1      #These tools are already parallaized so leave this at 1
activeThreads = 0
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

        global wb_dir
        global DEM
        global CVA
        global RUGGED
        global SDOS
        global DFME
        global FPS
        global EXTRACTVALLEYS
        
        wbt = WhiteboxTools()
        wbt.set_whitebox_dir(wb_dir)

        #Input file
        inputdem = DEM + self.file
        
        #Output files
        outputCVA = CVA + self.file.replace('.dep', '.tif')
        outputRUGGED = RUGGED + self.file.replace('.dep', '.tif')
        outputSDOS = SDOS + self.file.replace('.dep', '.tif')
        outputDFME = DFME + self.file.replace('.dep', '.tif')
        inputsmoothDEM = FPS + self.file.replace('.dep', '.tif')
        outputValleys = EXTRACTVALLEYS + self.file.replace('.dep', '.tif')
        
        #Arguments
        args1 = ['--input="' + inputdem + '"',  '--output="' + outputCVA + '"', '--filter="' + '3'+ '"']
        args2 = ['--input="' + inputdem + '"',  '--output="' + outputRUGGED + '"']
        args3 = ['--input="' + inputdem + '"',  '--output="' + outputSDOS + '"', '--zfactor="' + '1'+ '"', '--filterx="' + '3'+ '"', '--filtery="' + '3'+ '"']
        args4 = ['--dem="' + inputdem + '"', '--output="' + outputDFME + '"' , '--filterx="' + '7'+ '"', '--filtery="' + '7'+ '"']
        args6 = ['--input="' + inputsmoothDEM + '"',  '--output="' + outputValleys + '"', '--variant="' + 'JandR' + '"', '--line_thin="' + 'True' + '"', '--filter="' + '5' + '"']

        try:
            #wbt.run_tool('CircularVarianceOfAspect', args1, callback)
            wbt.run_tool('RuggednessIndex', args2, callback)
            #wbt.run_tool('StandardDeviationOfSlope', args3, callback)
            wbt.run_tool('DevFromMeanElev', args4, callback)
            #wbt.run_tool('ExtractValleys', args6, callback)
        except:
            print('Unexpected error:', sys.exc_info()[0])
            raise

        activeThreads -= 1

for inputfile in os.listdir(DEM):
    if inputfile.endswith('.dep'):
        worker = workerThread(inputfile).start()

    while activeThreads >= maxThreads:
        pass
