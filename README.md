# DeepLabCut_ZED_related
Converting ZED camera data to real world coordinates and retrieve z-coordinate

## steps

1. Copy all dll’s from the ZED SDK into the folder where the python scripts are located

2. Create a virtual environment with opencv installed

3. Process files
For processing only one session:
‘depth_sensing5_3animals.py’ 
Or
‘depth_sensing5_2animals.py’ 

Give as arguments:
Filename(path) of xy_coordinates csv file
Filename(path) of svo file
Output filename(path) (csv)
 
Like this: 
python depth_sensing5_2animals.py xypath.csv svopath.svo outfile.csv

The output is also a csv file but in real world coordinates (i.e. coordinates relative to the left front top corner of the cage) 

Note: Camera height from cage ceiling is hard coded in the script. 

For batch processing:
‘batch_script2.py’ 
with 
‘depth_sensing5_3animals_batch.py’  
Or
‘depth_sensing5_2animals_batch.py’  

You import the depth sensing script into the batch script. The batch script operates on a folder you hard code in the batch script


Rogier Landman Broad Institute, MIT, 2022


