Resources
1 -https://github.com/tbepler/topaz
2-https://topaz-em.readthedocs.io/en/latest/?badge=latest
3-https://github.com/3dem/topaz
4- High-throughput cryo-EM structure determination of amyloids (DOI https://doi.org/10.1039/D2FD00034B)



Training a model
Make sure nothing is sourced: source ~/.bashrc
Load Topaz Filament enviroment: load-topaz-filament
Go to your relion root folder
Example: cd /2-IND-EM/southworth_lab/my-user-name/processing_data/dataset_01/relion
When you type "ls" you should see all the relion subfolders, such as "CtfFind", "Class2D", "Extract" and others.
ATTENTION: If you don't see any of these folders, you're in the wrong folder and things won't work.
Run the training script on "screen" or "tmux". You will need 2 input files: CtfFind/job001/micrographs_ctf.star and Select/job002/particles.star
Now run the command:
python /2-IND-EM/southworth_lab/reference/topaz-filament/current_scripts/topaz-filament_pick4all_v1.py CtfFind/job001/micrographs_ctf.star Select/job002/particles.star
Training should be done in 4-6h, but it could take longer.


Optimizing parameters
Run particle picking in a subset of micrographs
Example:
topaz extract "SUBSET_SCALED_MICROGRAPHS" --model TopazFilament/model_epoch10.sav --radius 12 --threshold -5 --up-scale 1 --batch-size 1 --min-radius 5 --max-radius 100 --step-radius 2 -f -fp -fl 35 --num-workers 1 --device 2 --output TopazFilament/topaz_picks_subset.txt
Optimize the following parameters: --radius;--threshold;--fl
Run on all the micrographs
topaz extract TopazFilament/PreProcessed/* --model TopazFilament/ model_epoch10.sav --radius 12 --threshold -5 --up-scale 1 --batch-size 1 --min-radius 5 --max-radius 100 --step-radius 2 -f -fl 35 --num-workers 1 --device 2 --output TopazFilament/topaz_picks_all.txt
Convert topaz coordinates to relion:
python /2-IND-EM/southworth_lab/reference/topaz-filament/topazfilament2Relion4.py "topaz_picks_optimized.txt" "micrographs_ctf.star"it
