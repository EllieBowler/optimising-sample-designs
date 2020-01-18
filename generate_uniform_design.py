### Main script for generating a uniform design
### File: generate_uniform_design.py
### Ellie Bowler
### contact: e.bowler@uea.ac.uk
### All code available at https://github.com/EllieBowler/
### This script places the specified number of sample sites (--nsp) in a study landscape given input habitat fragmentation maps. The aim is to uniformly sample the range of the metrics, while spacing sites as evenly as possible geographically.
###################################################################
## Usage:
# --save_folder is the name of the directory where outputs will be saved, in the results subfolder
# --hab_path is the name of the geo-referenced habitat map 
# --n_metrics is the number of fragmentation metrics you are interested in sampling
# 
# --mask_path is the name of the input mask (for example InvalidAreasMask.tif)
# --nsp is the number of sample points which should be an integer value
###################################################################
# Example making an 80 site uniform design with the example invalid areas mask saved in the raw data folder. Saving outputs to Uniform_Demo
# python generate_uniform_design.py 
###################################################################

from utils import get_file_info, plot_design, save_uniform
from uda import generate_uniform_design
import os
import click

# Arguments used to call the method from the command line
@click.command('--save_folder', type=str, default='Stratified_Design', help='Specify the name of the folder where results will be saved')
@click.command('--n_metrics', type=int, default=1, help='The number of fragmentation metric maps you will be inputting')
@click.command('metric1', type=str, default='raw/DistanceToEdgeLog2.tif', help='Specify path and name of metric')
@click.command('metric2', type=str, default='raw/FragmentAreaLog10.tif', help='Specify path and name of metric')
@cilck.command('--mask_path', type=str, default='raw/InvalidAreasMask.tif', help='Specify path and name of the invalid areas mask')
@click.command('--nsp', type=int, default=30, help='Specify an integer number of sample sites')


def generate_design():
    
    # make results folder to save output
    savepath = 'results/{}'.format(save_folder)
    if not os.path.exists(savepath):
        os.mkdir(savepath)

    # get geo info and mask from tif file
    mask, nbins, res, GeoT, auth_code = get_file_info(mask_path)

    # generate design
    x_unif, y_unif = generate_uniform_design(mask, nsp)

    # plot design in pop up
    plot_design(mask, x_unif, y_unif)

    # save results to csv
    save_uniform(x_unif, y_unif, GeoT, auth_code, savepath, nsampled=0, updated='')

    return

if __name__ == '__main__':
    generate_design()
    

