# Main script for generating a uniform design
# File: generate_uniform_design.py
# Author: Ellie Bowler
# Contact: e.bowler@uea.ac.uk
# All code available at https://github.com/EllieBowler/
# This script places sample sites in a study landscape given input habitat fragmentation maps.
# The aim is to uniformly sample the range of the metrics, while spacing sites as evenly as possible geographically.
###################################################################
# Usage:
# --save_folder is the name of the directory where outputs will be saved, in the results subfolder
# --hab_path is the name of the geo-referenced habitat map 
# --n_metrics is the number of fragmentation metrics you are interested in sampling
# --mask_path is the name of the input mask (for example InvalidAreasMask.tif)
# --nsp is the number of sample points which should be an integer value
###################################################################
# Example command line input for an 80 site uniform design with the example metrics provided...
# python generate_uniform_design.py --metrics=raw/FragmentAreaLog10.tif --bins=7
# --metrics=raw/DistanceToEdgeLog2.tif --bins=6
###################################################################

from utils import get_file_info, plot_uniform, save_uniform, extract_raster
from uda import generate_uniform_design, bin_metrics, generate_all_layers, generate_id_im, generate_id_list
import os
import numpy as np
import click
from matplotlib import pyplot as plt


# Arguments used to call the method from the command line
@click.command()
@click.option('--save_folder', type=str, default='Uniform_Design', help='Name of folder where results will be saved')
@click.option('--hab_path', type=str, default='raw/HabitatMap.tif', help='Path to categorical habitat map')
@click.option('--metrics', multiple=True, help='Specify path and name of metric')
@click.option('--bins', multiple=True, help='Number of bins to break each metric into')
@click.option('--mask_path', type=str, default=None, help='Specify path and name of the invalid areas mask')
@click.option('--nsp', type=int, default=30, help='Specify an integer number of sample sites')
def generate_design(save_folder, hab_path, metrics, bins, mask_path, nsp):

    # make results folder to save output
    save_path = 'results/{}'.format(save_folder)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    # get geo info and habitat map from tif file
    habmap, n_bins, res, geo_t, prj_info = get_file_info(hab_path)

    if mask_path is not None:
        mask = extract_raster(mask_path)
    else:
        mask = np.ones((habmap.shape[0], habmap.shape[1]))

    metric_list = [habmap]
    bins_list = [n_bins]

    for i in range(len(metrics)):
        metric = extract_raster(metrics[i])
        metric_list.append(metric)
        bins_list.append(int(bins[i]))

    binned_metrics, combo_df, bin_breaks = bin_metrics(metric_list, mask, bins_list)
    all_layers, id_df, s_opt = generate_all_layers(binned_metrics, mask, combo_df, nsp)
    id_im, unique_ids = generate_id_im(all_layers, id_df)
    id_mix, id_df = generate_id_list(unique_ids, s_opt, nsp, id_df)

    print(id_df.head())

    # generate design
    x_unif, y_unif = generate_uniform_design(id_mix, id_im)

    # plot design in pop up
    plot_uniform(id_im, mask, x_unif, y_unif)

    # save results to csv
    save_uniform(x_unif, y_unif, id_mix, id_df, id_im, prj_info, geo_t, save_path)

    return


if __name__ == '__main__':
    generate_design()
