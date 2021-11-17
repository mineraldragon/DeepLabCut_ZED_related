#import sys
#sys.path.insert(0, '/location/of/subscripts')

import depth_sensing4c
import os, re

os.chdir(os.path.dirname(os.path.abspath(__file__)))

DLC_tag = "DLC_resnet50_OSTN-baselineApr11shuffle1_500000"
basedir = "F:\\Amelia"
svo_dir=basedir + "\\SVOs\\"

#xy_filepath_arr=[]
#outputfilename_arr=[]
#svofilename_arr=[]

for root, dir, file in os.walk(basedir):
    for f in file:
        if re.match('.*000.csv$', f):
            #rec_date
            tmp = f.index(DLC_tag)
            rec_date = f[:tmp]
            #xy_filepath_arr
            svofilename = basedir + "\\SVOs\\" + rec_date + ".svo"
            if os.path.exists(svofilename):
                xy_filepath  = basedir + "\\mp4s\\" + rec_date + DLC_tag + ".csv"
                #xy_filepath_arr.append(xy_filepath)
                #svofilename_arr.append(svofilename)
                outputfilename = basedir + "\\mp4s\\" + rec_date + "_cage_coordinates.csv"
                #outputfilename_arr.append(outputfilename)
                if not os.path.exists(outputfilename):   
                    depth_sensing4c.main(xy_filepath, svofilename, outputfilename)

                                            
#print(xy_filepath_arr)
#print(svofilename_arr)
#print(outputfilename_arr)
            
#rec_date = "11-14-20-Crocus"
#xy_filepath  = basedir + "\\mp4s\\" + rec_date + DLC_tag + ".csv"
#outputfilename = basedir + "\\mp4s\\" + rec_date + "_cage_coordinates.csv"
#svofilename = basedir + "\\SVOs\\" + rec_date + ".svo"

#depth_sensing4b.main(xy_filepath, svofilename, outputfilename)
