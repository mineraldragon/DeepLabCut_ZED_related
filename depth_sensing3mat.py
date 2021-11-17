import pyzed.sl as sl
import math
import numpy as np
import sys
import csv
import scipy.io
from tqdm import tqdm
import pandas as pd

def read_xy_mat(xy_filepath):
    mat = scipy.io.loadmat(xy_filepath)
    #xy_M1 = mat['A1']
    #xy_M2 = mat['A2']
    xy_M1 = mat['HeadBlue_mean']
    xy_M2 = mat['Head_mean']

    x_pixel_M1 = [item[0] for item in xy_M1]
    y_pixel_M1 = [item[1] for item in xy_M1]
    x_pixel_M2 = [item[0] for item in xy_M2]
    y_pixel_M2 = [item[1] for item in xy_M2]
    # return (xy_M1, xy_M2)
    
    return(x_pixel_M1, y_pixel_M1, x_pixel_M2, y_pixel_M2) 

def read_xy_csv(xy_filepath):

    print("reading " + xy_filepath)
    csv_data = pd.read_csv(xy_filepath, header=None, skiprows=3)

    csv_data = csv_data.astype(float)
    csv_data = csv_data.astype(int)    
    csv_data[csv_data < 1] = 1

    #x_pixel_M1head = csv_data[7][:].tolist()
    #y_pixel_M1head = csv_data[8][:].tolist()    
    
    #x_pixel_M2head = csv_data[19][:].tolist()
    #y_pixel_M2head = csv_data[20][:].tolist()    


    x_pixel_M1head = csv_data[1][:].tolist()
    y_pixel_M1head = csv_data[2][:].tolist()    
    
    x_pixel_M2head = csv_data[4][:].tolist()
    y_pixel_M2head = csv_data[5][:].tolist()  

    return(x_pixel_M1head, y_pixel_M1head, x_pixel_M2head, y_pixel_M2head)
        

def extract_xyz(x_pixel_M1, y_pixel_M1, x_pixel_M2, y_pixel_M2, outputfilename, svofilename):
    x_world_M1 = []
    y_world_M1 = []
    z_world_M1 = []
    x_world_M2 = []
    y_world_M2 = []
    z_world_M2 = []

    x_pixel_M1 = np.abs(x_pixel_M1)
    y_pixel_M1 = np.abs(y_pixel_M1) 
    x_pixel_M2 = np.abs(x_pixel_M2)
    y_pixel_M2 = np.abs(y_pixel_M2) 
    # x_pixel_M1 = [item[8] for item in xy_M1]
    # y_pixel_M1 = [item[9] for item in xy_M1]
    # x_pixel_M2 = [item[8] for item in xy_M2]
    # y_pixel_M2 = [item[9] for item in xy_M2]

    #filepath = "/home/avnish/zed_marmoset_recording/20200922.svo"
    #print("SVO file : ", filepath.rsplit('/', 1)[1])
    # Create a Camera object

    # Create a InitParameters object and set configuration parameters
    #init_params = sl.InitParameters(svo_input_filename=filepath,svo_real_time_mode=False)
    
    #InitParameters init_params; // Set initial parameters
    #init_params.sdk_verbose = True; // Enable verbose mode
    #init_params.input.setFromSVOFile("/path/to/file.svo"); // Selects the and SVO file to be read

    

    input_type = sl.InputType()
    print("reading " + svofilename)
    input_type.set_from_svo_file(svofilename)
    init = sl.InitParameters(input_t=input_type, svo_real_time_mode=False)
    init.depth_mode = sl.DEPTH_MODE.ULTRA
    init.coordinate_units = sl.UNIT.MILLIMETER  # Use milliliter units (for depth measurements)
    #init.depth_minimum_distance = 300
    #init.depth_maximum_distance = 1500

    zed = sl.Camera()

    # Open the camera
    err = zed.open(init)
    if err != sl.ERROR_CODE.SUCCESS:
        print('error_details: ', repr(err))
        exit(1)

    # Create and set RuntimeParameters after opening the camera
    runtime_parameters = sl.RuntimeParameters()
    runtime_parameters.sensing_mode = sl.SENSING_MODE.FILL
    #runtime_parameters.sensing_mode = sl.SENSING_MODE.SENSING_MODE_FILL  # Use STANDARD sensing mode

    i = 0
    pbar = tqdm(total=len(x_pixel_M1))
    # image = sl.Mat()
    point_cloud = sl.Mat()

    try:    
        #while i < len(x_pixel_M1):
        while i < 1000:
        # A new image is available if grab() returns SUCCESS
            if zed.grab(runtime_parameters) == sl.ERROR_CODE.SUCCESS:
                # Retrieve left image
                # zed.retrieve_image(image, sl.VIEW.VIEW_LEFT)
                # Retrieve depth map. Depth is aligned on the left image
                # zed.retrieve_measure(depth, sl.MEASURE.MEASURE_DEPTH)
                zed.retrieve_measure(point_cloud, sl.MEASURE.XYZRGBA)
                #print(x_pixel_M1[i], y_pixel_M1[i], x_pixel_M2[i], y_pixel_M2[i])
                #print(type(x_pixel_M1[i]))
                   
                err_M1, point_cloud_value_M1 = point_cloud.get_value(x_pixel_M1[i], y_pixel_M1[i])
                err_M2, point_cloud_value_M2 = point_cloud.get_value(x_pixel_M2[i], y_pixel_M2[i])
                #print('after get value')                
                # Get and print distance value in mm at the center of the image
                # We measure the distance camera - object using Euclidean distance
                # x = round(image.get_width() / 2)
                # y = round(image.get_height() / 2)

                lens2cage_top_mm=693.42
                lens2cage_edge_x_mm=387.35
                lens2cage_edge_y_mm=387.35
                x_world_M1.append(point_cloud_value_M1[0] + lens2cage_edge_x_mm) #millimeters; in cage coordinates
                y_world_M1.append(-point_cloud_value_M1[1] + lens2cage_edge_y_mm)
                z_world_M1.append(point_cloud_value_M1[2] - lens2cage_top_mm)
                x_world_M2.append(point_cloud_value_M2[0] + lens2cage_edge_x_mm)
                y_world_M2.append(-point_cloud_value_M2[1] + lens2cage_edge_y_mm)
                z_world_M2.append(point_cloud_value_M2[2] - lens2cage_top_mm)


                # Increment the loop
                # print(i)
                pbar.update(1)
                i += 1
                # if (i % 1000) == 0:
                # print(i)
                # sys.stdout.flush()
    
        pbar.close()
        # Close the camera
        zed.close()

    except OverflowError as error:
        print(error)
        print("frame_number_completed: {}".format(i))
        pbar.close()
        zed.close()

    finally:
        rows = zip(x_world_M1, y_world_M1, z_world_M1, x_world_M2, y_world_M2, z_world_M2)
        print("writing " + outputfilename)
        with open(outputfilename, 'w') as f:
            writer = csv.writer(f)
            for row in rows:
                writer.writerow(row)
        print("Done")

if __name__ == "__main__":
    rec_date="20191120"
    basedir="D:\\Data\\" + rec_date + "\\" + rec_date + "\\"
    #xy_filepath  = basedir + "will_tracker_files\\output\\" + rec_date + "DeepCut_resnet50_reachingJan30shuffle1_200000.csv" 
    #xy_filepath  = basedir + "will_tracker_files\\output\\" + rec_date + "DLC_resnet50_ZED_2_ptDec2shuffle1_200000filtered.csv" 
    xy_filepath  = basedir + "will_tracker_files\\output\\2019_11_20.mat"
    #"20190920DLC_resnet50_ZED_2_ptDec2shuffle1_200000filtered.csv"
    outputfilename = "D:\\Data\\RWC_csv\\" + rec_date + "_cage_coordinates.csv"
    svofilename = basedir + "SVO_files\\" + rec_date + ".svo"
    #xy_filepath  = "/media/avnish/Data/zed_marmoset_recording/20191115/will_tracker_files/output/2019_11_15.mat" 
    #xy_M1, xy_M2 = read_xy_mat(xy_filepath)
    x_pixel_M1head, y_pixel_M1head, x_pixel_M2head, y_pixel_M2head = read_xy_mat(xy_filepath)
    #x_pixel_M1head, y_pixel_M1head, x_pixel_M2head, y_pixel_M2head = read_xy_csv(xy_filepath)
    extract_xyz(x_pixel_M1head, y_pixel_M1head, x_pixel_M2head, y_pixel_M2head, outputfilename, svofilename)