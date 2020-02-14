import numpy as np
from random import randint
from scipy import ndimage
from copy import copy


def update_stratified_design(mask, sampled_csv):
    """
    Main function for updating an existing or partially completed sample design, when certain sites are inaccessible.
    Takes as inputs an updated invalid areas mask, and a .csv file showing already sampled sites.
    INPUTS:
        mask: (np.array) Invalid areas mask
        sampled_csv: (data frame) Tagged data frame output by the original stratified design
    OUTPUTS:
        x_vals: (list) x coordinates of sample sites
        y_vals: (list) y coordinates of sample sites
    """

    # Extract sampled site information from csv file
    nsp = len(sampled_csv)
    sampled_df = sampled_csv.loc[sampled_csv['sampled'] == 1]
    n_sampled = len(sampled_df)
    print('{} sites already sampled and will not be moved'.format(n_sampled))
    print('{} sites to be adjusted based on mask update'.format(nsp - n_sampled))

    # Initialise empty arrays and lists to save design
    imheight, imwidth = mask.shape
    sampled_x = sampled_df['row'].values.astype(int)
    sampled_y = sampled_df['col'].values.astype(int)

    sites = np.ones((imheight, imwidth))
    sites[sampled_x, sampled_y] = 0
    mask_aux = copy(mask)
    x_vals = [sampled_x]
    y_vals = [sampled_y]

    for i in range(nsp - n_sampled):
        print('Plotting site {} of {}'.format(i + 1, nsp - n_sampled))

        # Generate EDT image of all sampled/selected sites
        dist_im = ndimage.distance_transform_edt(sites)

        # Make all elements of EDT map in invalid region 0
        dist_im *= mask_aux

        # Extract coordinates of pixels with maximum distance value
        dist_mx = list(zip(*np.where(dist_im == dist_im.max())))

        # Choose one max coord pair at random
        idx = randint(0, len(dist_mx) - 1)
        x, y = dist_mx[idx]

        # Save x and y coordinates
        x_vals = np.append(x_vals, x)
        y_vals = np.append(y_vals, y)

        # Code chosen site to be zero in site array
        sites[x, y] = 0

    print('Adapted stratified design complete!')
    return x_vals, y_vals
