#### Script written by Carl Vigren, Research Assistant @ Swedish University of Agricultural Sciences, Umeå ####
##### Contact: carl.vigren@slu.se ######

library(dplyr)
library(data.table)
library(raster)
library(rgdal)
library(sp)
library(doParallel)
library(foreach)
#Build Cluster of all cores exceept one
UseCores <- detectCores() -1
#Register CoreCluster
cl       <- makeCluster(UseCores)
registerDoParallel(cl)

#all files in pathway
setwd("E:/DEM")
path       <- "E:/DEM"
stack_list <- list.files(path, pattern=".tif$", full.names=F) #the file ending is case sensetive ".TIF" and ".tif" is not the same.
stack_listoutname <- sub(stack_list,pattern=".tif",replacement="_X")

#Output directory
outpath <- "D:/MLWAM_Production/Rasters/Original/X_Coordinates_x/"
outfiles <- paste0(outpath, stack_listoutname)

#For each in list, import, save.
foreach(i=1:length(stack_list), .packages=c("foreach","doParallel","raster","sp","rgdal")) %dopar% {
  rasterdf  <- raster(paste0("E:/DEM/",stack_list[i]))
  ymatrix <- matrix(xFromCell(rasterdf,c(1:1562500)),nrow=1250,byrow=TRUE)
  ImgExtent <- extent(rasterdf)
  ymatrix <- raster(ymatrix)
  #crs(ymatrix)<- "+proj=utm +zone=33 +ellps=GRS80 +towgs84=0,0,0,0,0,0,0 +units=m +no_defs"
  ymatrixcorrectextent<- setExtent(x= ymatrix, ext=ImgExtent, keepres=FALSE,snap = TRUE)
  writeRaster(ymatrixcorrectextent,
              filename=outfiles[i],
              overwrite=T,
              format="GTiff")
  }

#end cluster
stopCluster(cl)
