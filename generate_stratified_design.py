### Main script for generating a stratified design ###

from utils import get_file_info, plot_design, Save_Stratified
from sda import generate_stratified_design
import os

# Specify name for project - this folder will be created in the results folder, and
# all outputs saved in this directory, e.g:
save_folder = 'Stratified_Design_Test'

# Enter path to invalid areas masked (saved in the 'raw' data folder), e.g:
mask_path = 'raw/InvalidAreasMask.tif'

# Enter an integer number of sample sites, e.g:
nsp = 30


def main():
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

main()




