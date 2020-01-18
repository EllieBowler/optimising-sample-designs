### Main script for updating a stratified design
### NOTE: THIS CODE REQUIRES AN EXISTING STRATIFIED DESIGN (generate_stratified_design.py)
### File: update_stratified_design_opt1.py
### Ellie Bowler
### contact: e.bowler@uea.ac.uk
### All code available at https://github.com/EllieBowler/
### This script updates a stratified design by shifting points based in new innaccessible locations. Sites which have already been sampled remain in the same location.
###################################################################
## Usage:
# --save_folder is the name of the directory where outputs will be saved, in the results subfolder
# --updated_mask_path is the name of the input mask (for example InvalidAreasMask.tif)
# --csv_path csv file output by the original stratified design, with sampled column tagged
###################################################################
# Example adapting design generated using the test data
# python update_stratified_design_opt1.py --save_folder AdaptedStratified30 --updated_mask_path raw/InvalidAreasMask_updated.tif --csv_path results
###################################################################

from utils import get_file_info, plot_design, save_stratified
from sda import update_stratified_design
import os
import click


@click.command()
@click.option('--save_folder', type=str, default='Stratified_Adapted', help='Specify the name of the folder where results will be saved')
@click.option('--updated_mask_path', type=str, default='raw/InvalidAreasMask_updated.tif', help='Specify path and name of the invalid areas mask')
@click.option('--csv_path', type=int, default=30, help='Specify an integer number of sample sites')
def generate_design(save_folder, updated_mask_path, csv_path):

    # make results folder to save output
    save_path = 'results/{}'.format(save_folder)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # get geo info and mask from path
    mask, nbins, res, GeoT, auth_code = get_file_info(mask_path)

    # generate design
    x_strat, y_strat = update_stratified_design(mask, nsp, sampled_df)

    # plot design in pop up
    plot_design(mask, x_strat, y_strat)

    # save results to csv
    save_stratified(x_strat, y_strat, GeoT, auth_code, save_path, nsampled=0, updated='')

    return


if __name__ == '__main__':
    generate_design()
