### Main script for generating a stratified design ###

from utils import get_file_info, plot_design, Save_Stratified
from sda import generate_stratified_design
import os
import click

@click.command('--save_folder', type=str, default='Stratified_Design', help='Specify the name of the folder where results will be saved')
@cilck.command('--mask_path', type=str, default='raw/InvalidAreasMask.tif', help='Specify path and name of the invalid areas mask')
@click.command('--nsp', type=int, default=30, help='Specify an integer number of sample sites')

# # Specify name for project - this folder will be created in the results folder, and
# # all outputs saved in this directory, e.g:
# save_folder = 'Stratified_Design_Test'

# # Enter path to invalid areas masked (saved in the 'raw' data folder), e.g:
# mask_path = 'raw/InvalidAreasMask.tif'

# # Enter an integer number of sample sites, e.g:
# nsp = 30


def generate_design():
    # make results folder to save output
    savepath = 'results/{}'.format(save_folder)

    if not os.path.exists(savepath):
        os.mkdir(savepath)

    # get geo info and mask from path
    mask, nbins, res, GeoT, auth_code = get_file_info(mask_path)

    # generate design
    x_strat, y_strat = generate_stratified_design(mask, nsp)

    # plot design in pop up
    plot_design(mask, x_strat, y_strat)

    # save results to csv
    Save_Stratified(x_strat, y_strat, GeoT, auth_code, savepath, nsampled=0, updated='')

    return

if __name__ == '__main__':
    generate_design()
    




