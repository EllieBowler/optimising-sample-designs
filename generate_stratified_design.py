### Main script for generating a stratified design
### File: generate_stratified_design.py
### Ellie Bowler
### contact: e.bowler@uea.ac.uk
### All code available at https://github.com/EllieBowler/
### This script distributes the specified number of sample sites (--nsp) evenly over a given sample landscape.
### This landscape is represented by a binary (0 = invalid, 1 = valid) geo-referenced satellite image.
### For an example image please see InvalidAreasMask.tif in the raw data folder.
###################################################################
## Usage:
# --save_folder is the name of the directory where outputs will be saved, in the results subfolder
# --mask_path is the name of the input mask (for example InvalidAreasMask.tif)
# --nsp is the number of sample points which should be an integer value
###################################################################
# Example making a 30 site stratified design with the example invalid areas mask saved in the raw data folder,
# saving outputs to Stratified_Design_Demo
# python generate_stratified_design.py --save_folder Stratified_Design_Demo --mask_path raw/InvalidAreasMask.tif --nsp 30
###################################################################

from utils import get_file_info, plot_design, save_stratified
from sda import generate_stratified_design
import os
import click


# Arguments used to call the method from the command line
@click.command()
@click.option('--save_folder', type=str, default='Stratified_Design',
               help='Specify the name of the folder where results will be saved')
@click.option('--mask_path', type=str, default='raw/InvalidAreasMask.tif',
               help='Specify path and name of the invalid areas mask')
@click.option('--nsp', type=int, default=30, help='Specify an integer number of sample sites')
def generate_design(save_folder, mask_path, nsp):
    
    # make results folder to save output
    save_path = 'results/{}'.format(save_folder)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # get geo info and mask from tif file
    mask, nbins, res, GeoT, auth_code = get_file_info(mask_path)

    # generate design
    x_strat, y_strat = generate_stratified_design(mask, nsp)

    # plot design in pop up
    plot_design(mask, x_strat, y_strat)

    # save results to csv
    save_stratified(x_strat, y_strat, GeoT, auth_code, save_path, nsampled=0, updated='')

    return


if __name__ == '__main__':
    generate_design()
