import os

#This is where all the clipped raster files are saved
folderwithfiles = 'D:/WilliamLidberg/FeatureExtraction/SplittedDEM/Raster'
#This loop will find all files that ends with .tif and join them to their path
#First make a empty list
listofrasters = []

#Then look for tif files in the folderwithfiles 
for root, dirs, files in os.walk(os.path.abspath(folderwithfiles)):
    for file in files:
        if file.endswith('.tif'):
            listofrasters.append(os.path.join(root, file))

#Save list to text file that whitebox GAt can read.            
with open('listofrasterstoimport.txt','w')as output:
    output.write('\n'.join(listofrasters))

