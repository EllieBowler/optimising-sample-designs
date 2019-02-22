# Main code for updating an existing or partially completed sample design, when certain sites are inaccessible.
# Takes as inputs an updated invalid areas mask, and a .csv file showing already sampled sites.

import numpy as np
from random import randint
from scipy import ndimage
from copy import copy


def update_stratified_design(mask, nsp, sampled_df):
    """
    Update an existing sample design using a revised invalid areas mask.
    INPUTS:
        mask: (.tif) Binary invalid areas mask of size (imheight, imwidth) showing areas which should not be sampled
        nsp: (integer) Desired number of sample sites
        sampled_df: (.csv) The csv output by the original stratified design, with tagged sampled and unsampled sites
    OUTPUTS:
        xy0: (.npy) A (2, nsp) dimension list of x, y coordinates for the chosen sample sites
    """

    imheight, imwidth = mask.shape
    nsampled = len(sampled_df)
    sampled_x = sampled_df['row'].values
    sampled_y = sampled_df['col'].values

    sites = np.ones((imheight, imwidth))
    sites[sampled_x, sampled_y] = 0
    mask_aux = copy(mask)
    x_vals = [sampled_x]
    y_vals = [sampled_y]

    for i in range(nsp - nsampled):


        # Generate EDT image of all sampled/selected sites
        dist_im = ndimage.distance_transform_edt(sites) * mask
        # Extract coordinates with the maximum distance value
        dist_mx = zip(*np.where(dist_im == dist_im.max()))

        # Choose one maximum coord pair at random
        idx = randint(0, len(dist_mx) - 1)
        x, y = dist_mx[idx]

        # Make all elements of EDT map in invalid region 0
        dist_im = dist_im * mask_aux
        # Extract coords of pixels with maximum distance value
        dist_mx = zip(*np.where(dist_im == dist_im.max()))

        # Choose one max coord pair at random
        idx = randint(0, len(dist_mx) - 1)
        x, y = dist_mx[idx]

        # Save x and y coords
        x_vals = np.append(x_vals, x)
        y_vals = np.append(y_vals, y)

        # Code chosen site to be zero (a feature pixel) in site array
        sites[x, y] = 0

        # Update the euclidean distance transform
        # dist_im = ndimage.distance_transform_edt(sites)
    xy0 = np.hstack([x_vals, y_vals])
    return xy0