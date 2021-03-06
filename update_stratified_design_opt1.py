# Main script for updating a stratified design, using an updated mask
# NOTE: THIS CODE REQUIRES AN EXISTING STRATIFIED DESIGN (generate_stratified_design.py)
# File: update_stratified_design_opt1.py
# Author: Ellie Bowler
# Contact: e.bowler@uea.ac.uk
# All code available at https://github.com/EllieBowler/
# This script updates a stratified design by shifting points based in new inaccessible locations.
# Sites which have already been sampled remain in the same location.
###################################################################
# Usage:
# --save_folder is the name of the directory where outputs will be saved, in the results sub-folder
# --updated_mask_path is the name of the updated mask file (for example InvalidAreasMask_updated.tif)
# --csv_path csv file output by the original stratified design, sampled sites should be tagged with a one
###################################################################
# Example adapting design generated using the test data
# python update_stratified_design_opt1.py --save_folder=Stratified_Adapted
# --updated_mask_path=input/InvalidAreasMask_updated.tif --csv_path=results/30site_strat_tagged_opt1.csv
###################################################################

from utils import get_file_info, plot_adapted_stratified, save_stratified
from sda import update_stratified_design
import os
import click
import pandas as pd


@click.command()
@click.option('--save_folder', type=str, default='Stratified_Adapted', help='Name folder where results will be saved')
@click.option('--updated_mask_path', type=str, default='input/InvalidAreasMask_updated.tif', help='Path and name of updated invalid areas mask')
@click.option('--csv_path', type=str, default='results/30site_strat_tagged_opt2.csv', help='Path to tagged csv file')
def generate_design(save_folder, updated_mask_path, csv_path):

    # make results folder to save output
    save_path = 'results/{}'.format(save_folder)
    if not os.path.exists(save_path):
        os.mkdir(save_path)
    print('Results will be saved to {}'.format(save_path))

    # get geo info and mask from path
    updated_mask, n_bins, res, geo_t, prj_info = get_file_info(updated_mask_path)
    sampled_csv = pd.read_csv(csv_path)

    # generate design
    x_adpt, y_adpt = update_stratified_design(updated_mask, sampled_csv)

    # plot design in pop up
    plot_adapted_stratified(updated_mask, x_adpt, y_adpt, sampled_csv)

    # save results to csv
    save_stratified(x_adpt, y_adpt, prj_info, geo_t, save_path, sampled_csv)
    return


if __name__ == '__main__':
    generate_design()
