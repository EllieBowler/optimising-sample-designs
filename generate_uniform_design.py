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

from utils import get_file_info, plot_design, save_uniform, extract_raster
from uda import generate_uniform_design, bin_metrics
import os
import numpy as np
import click

# Arguments used to call the method from the command line
@click.command()
@click.option('--save_folder', type=str, default='Stratified_Design', help='Specify the name of the folder where results will be saved')
# @click.option('--n_metrics', type=int, default=1, help='The number of fragmentation metric maps you will be inputting'
@click.option('--habmap_path', type=str, default='raw/HabitatMap.tif', help='Path to categorical habitat map')
@click.option('--metrics', type=list, default=['raw/DistanceToEdgeLog2.tif', 'raw/FragmentAreaLog10.tif'],
                                              help='Specify path and name of metric')
@click.option('--bins', type=list, default=[10, 8])
# @click.option('--metric2', type=str, default='raw/FragmentAreaLog10.tif', help='Specify path and name of metric')
@click.option('--mask_path', type=str, default='raw/InvalidAreasMask.tif', help='Specify path and name of the invalid areas mask')
@click.option('--nsp', type=int, default=30, help='Specify an integer number of sample sites')
def generate_design(save_folder, habmap_path, metrics, bins, mask_path, nsp):
    
    # make results folder to save output
    save_path = 'results/{}'.format(save_folder)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # get geo info and habitat map from tif file
    habmap, nbins, res, GeoT, auth_code = get_file_info(habmap_path)

    if mask_path.exists():
        mask = extract_raster(mask_path)
    else:
        mask = np.ones((habmap.shape[0], habmap.shape[1]))

    metric_list = [habmap]
    bins_list = [nbins]

    for i in range(len(metrics)):
        metric = extract_raster(metrics[i])
        metric_list.append(metric)
        bins_list.append(bins[i])

    binned_metrics, combo_df, bin_breaks = bin_metrics(metric_list, mask, bins_list)
    all_layers, ID_df, s_opt = generate_all_layers(binned_metrics, mask, combo_df, nsp)
    store_masks, ID_im, unique_IDs = generate_ID_im(all_layers, ID_df, nsp, save_path)
    id_mix, ID_df = generate_id_list(unique_IDs, s_opt, nsp, ID_df)

    # generate design
    x_unif, y_unif = generate_uniform_design(id_mix, unique_IDs, store_masks)

    # plot design in pop up
    plot_design(habmap, x_unif, y_unif)

    # save results to csv
    save_uniform(x_unif, y_unif, GeoT, auth_code, save_path, nsampled=0, updated='')

    return


if __name__ == '__main__':
    generate_design()
