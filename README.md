# Digital_Soil_Mapping
Can soil types be extracted from LiDAR point clouds?

![alt text](DigitalElevationModel.png)

1. INTRODUCTION
Digital soil mapping has moved from research to implementation and machine learning has become an important part of digital soil mapping. Machine learning or statistical learning is when data is used to train a model instead of programming it manually. Machine learning is often referred to as a Black box. A Black Box is a system that does not reveal its internal mechanisms. In machine learning, a “black box” describes models that cannot be understood by looking at their parameters. The opposite of a black box is sometimes referred to as White Box. In fact, Whitebox is the name of the geoprocessing software used for most features in this project and it got its name from the open-access philosophy used in its development. Machine learning and statistics have somewhat different terminology so here is a shortlist of names used: 
Model is a trained machine learning algorithm 
Features are the columns in the training data. In our case, it will be “Elevation”, “topography” etc.
Target is what the model is trying to predict. In our case, it will be soil classes.
2. METHOD
The method consists of two major steps: 1 feature extraction and 2 machine learning and prediction. The Feature extraction is mostly done using GIS and python while the machine learning and prediction is done using R.

