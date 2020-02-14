# Main script for updating a stratified design, excluding areas around tagged sites
# NOTE: THIS CODE REQUIRES AN EXISTING STRATIFIED DESIGN (generate_stratified_design.py)
# File: update_stratified_design_opt2.py
# Author: Ellie Bowler
# contact: e.bowler@uea.ac.uk
# All code available at https://github.com/EllieBowler/
# This script updates a stratified design by shifting points based in new inaccessible locations.
# Sites which have already been sampled remain in the same location.
###################################################################
# Usage:
# --save_folder is the name of the directory where outputs will be saved, in the results sub-folder
# --original_mask_path is the name of the input mask (for example InvalidAreasMask.tif)
# --csv_path csv file output by the original stratified design, with sampled column tagged. Tags are:
#       1 : If site has already been sampled successfully
#       2 : If the site is inaccessible, and you wish to exclude a radius around it
#       0 : Any sites which have not been sampled
# --radius is the radius to exclude around inaccessible sites (in metres)
###################################################################
# Example adapting design generated using the test data
# python update_stratified_design_opt2.py --save_folder=Stratified_Adapted --original_mask_path=raw/InvalidAreasMask.tif
# --csv_path=results/30site_strat_tagged_opt2.csv --radius=1000
###################################################################

from utils import get_file_info, plot_adapted_stratified, save_stratified, update_mask
from sda import update_stratified_design
import os
import click
import pandas as pd


@click.command()
@click.option('--save_folder', type=str, default='Stratified_Adapted', help='Name folder where results will be saved')
@click.option('--original_mask_path', type=str, default='raw/InvalidAreasMask.tif', help='Path and name of invalid areas mask')
@click.option('--csv_path', type=str, default='results/30site_strat_tagged_opt2.csv', help='Path to tagged csv file')
@click.option('--radius', type=float, default=3000, help='Radius to exclude around tagged points (in metres)')
def generate_design(save_folder, original_mask_path, csv_path, radius):

    # make results folder to save output
    save_path = 'results/{}'.format(save_folder)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # get geo info and mask from path
    original_mask, n_bins, res, geo_t, prj_info = get_file_info(original_mask_path)
    sampled_csv = pd.read_csv(csv_path)

    updated_mask = update_mask(sampled_csv, original_mask, radius, res)

    # generate design
    x_adpt, y_adpt = update_stratified_design(updated_mask, sampled_csv)

    # plot design in pop up
    plot_adapted_stratified(updated_mask, x_adpt, y_adpt, sampled_csv)

    # save results to csv
    save_stratified(x_adpt, y_adpt, prj_info, geo_t, save_path, sampled_csv)
    return


if __name__ == '__main__':
    generate_design()
