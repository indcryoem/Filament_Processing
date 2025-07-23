#!/usr/bin/env python3

import starfile
import pandas as pd
import numpy as np
import os
import argparse
from datetime import date


###########
#variables#
###########
parser = argparse.ArgumentParser("topazfilament2Relion4.py")
parser.add_argument("input01", help="topaz_picks_optimized.txt", type=str)
parser.add_argument("input02", help="micrographs_ctf.star", type=str)
args = parser.parse_args()


#Input for the script
topaz_picks=args.input01
input_mics=args.input02


#Read both files into DataFrame
df = pd.read_csv(topaz_picks,delim_whitespace=True)
star_ctf = starfile.read(input_mics)



#Get prefix and suffix from files
mics = star_ctf["micrographs"]['rlnMicrographName']
for n,micrograph in enumerate(mics):
    prefix,mic_name = micrograph.split(sep='/')
    file_path,ext = micrograph.split(sep='DW.')
    
if os.path.isdir(prefix):
    print('Folder ' ,prefix,' exist.')
else:
    command_mkdir = 'mkdir {}'.format(prefix)
    os.system(command_mkdir)
    
#Add prefix and suffix to image_name
new_star = pd.DataFrame((),columns=["rlnMicrographName","rlnCoordinateX","rlnCoordinateY"])
mic_full_name = []
x_coordinate = []
y_coordinate = []
for n,line in enumerate(df.index):
    name = '{}/{}.{}'.format(prefix,df.image_name[n],ext)
    mic_full_name.append(name)

new_star.rlnMicrographName = mic_full_name
new_star.rlnCoordinateX = df.x_coord*8
new_star.rlnCoordinateY = df.y_coord*8


#Create topaz_star_files from new_star
mic_name = new_star.rlnMicrographName
coordX = new_star.rlnCoordinateX
coordY = new_star.rlnCoordinateY
umic= mic_name.unique()
np.size(umic)


for name in umic:
    filename = name + '_topazpick.star'
    df2 = new_star.loc[new_star['rlnMicrographName'] == name]
    starfile.write(df2,filename,overwrite=True)
    
    
df3 = pd.DataFrame((),columns=['rlnMicrographName','rlnMicrographCoordinates'])
coords_list =[]
mics_list =[]

topazpicks_abs_path = os.path.abspath(topaz_picks)
separated = topazpicks_abs_path.split(sep='/')
folder01 = separated[-2]
coords_prefix = '{}/'.format(folder01)
#might not work


for name in umic:
    coords = name + '_topazpick.star'
    mic = name
    coords_list.append(coords)
    mics_list.append(mic)
df3['rlnMicrographName']=mics_list
df3['rlnMicrographCoordinates']=coords_list

#output_file
today = date.today()
username = os.getlogin()
out_star = 'topaz_filament_START-ENDcoordinates_for_Relion4_{}_{}.star'.format(str(username),str(today))
starfile.write(df3,out_star,overwrite=True)
