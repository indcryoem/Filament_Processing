import os
from datetime import date
import argparse

parser = argparse.ArgumentParser("train_model_topaz-filament.py")
parser.add_argument("input01", help="micrographs_ctf.star", type=str)
parser.add_argument("input02", help="particles.star", type=str)
args = parser.parse_args()


#Input for the script
input_mics=args.input01
input_picks=args.input02

#Input files
micrographs_ctf = input_mics
input_particles = input_picks
output_folder = 'TopazFilament/'

#Create folder
if os.path.isdir(output_folder):
    print('Folder ' ,output_folder,' exist.')
else:
    command_mkdir = 'mkdir {}'.format(output_folder)
    os.system(command_mkdir)

#Convert particles.star from Relion to Topaz format
cmd1 = 'python /2-IND-EM/southworth_lab/amelo/programs/topaz/Step1.py -i {} --inputpart {} -s 8 -o {} --topaz_path topaz'.format(micrographs_ctf,input_particles,output_folder)
print("Converting particles from Relion format to Topaz format for training a model")
os.system(cmd1)

#Train model
model_out = 'TopazFilament/model_training.txt'
target = 'TopazFilament/inputparts_scaled.txt'
today = date.today()
cmd2 = 'topaz train -n 200 -r 4 -d 7 -o {} --num-threads=1 --num-workers=40 --train-images=TopazFilament/PreProcessed/ --train-targets={} --save-prefix=TopazFilament/{}_model'.format(model_out,target,today)
print('Training a topaz model using particles.star')
os.system(cmd2)



