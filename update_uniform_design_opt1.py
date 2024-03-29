### Main script for updating a uniform design
### NOTE: THIS CODE REQUIRES AN EXISTING STRATIFIED DESIGN (generate_stratified_design.py)
### File: update_stratified_design_opt1.py
### Ellie Bowler
### contact: e.bowler@uea.ac.uk
### All code available at https://github.com/EllieBowler/
### This script updates a uniform design by shifting points based in new innaccessible locations.
### Sites which have already been sampled remain in the same location.
###################################################################
## Usage:
# --save_folder is the name of the directory where outputs will be saved, in the results subfolder
# --updated_mask_path is the name of the input mask (for example InvalidAreasMask.tif)
# --csv_path csv file output by the original stratified design, with sampled column tagged
###################################################################
# Example adapting design generated using the test data
# python update_uniform_design_opt1.py --save_folder AdaptedStratified30 --updated_mask_path input/InvalidAreasMask_updated.tif --csv_path results
###################################################################

from utils import get_file_info, plot_design, save_uniform
from uda import update_uniform_design
import os
import click


@click.command()
@click.option('--save_folder', type=str, default='Stratified_Adapted', help='Specify the name of the folder where results will be saved')
@click.option('--updated_mask_path', type=str, default='input/InvalidAreasMask_updated.tif', help='Specify path and name of the invalid areas mask')
@click.option('--csv_path', type=int, default=30, help='Specify an integer number of sample sites')
def generate_design(save_folder, updated_mask_path, csv_path):

    # make results folder to save output
    save_path = 'results/{}'.format(save_folder)
    if not os.path.exists(save_path):
        os.mkdir(save_path)

    savefiles = np.load(npz_path)
    ID_im = savefiles['ID_im']
    metrics = savefiles['immetrics']
    binned_metrics = savefiles['binned_metrics']

    # get geo info and mask from path
    updated_mask, nbins, res, GeoT, auth_code = get_file_info(updated_mask_path)
    sampled_df, nsp, id_mix_unsampled, save_IDs, unique_IDs, nsampled = get_sampling_info(csv_path)

    store_masks = store_layers(ID_im, mask, unique_IDs)

    # generate design
    x_adpt, y_adpt = update_uniform_design(sampled_df, id_mix_unsampled, store_masks)

    # plot design in pop up
    plot_design(mask, x_adpt, y_adpt)

    # save results to csv
    save_uniform(x_adpt, y_adpt, GeoT, auth_code, save_path, nsampled=0, updated='')

    return


if __name__ == '__main__':
    generate_design()
