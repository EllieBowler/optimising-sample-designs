# Main code for generating a stratified design.
# Takes as inputs a binary mask for any invalid/ inaccessible regions, and the desired number of sample sites.
# Places sites iteratively at the maximum distance apart, spacing them evenly in the landscape.

import numpy as np
from random import randint
from scipy import ndimage
from copy import copy

def generate_stratified_design(mask, nsp):
    """"
    Generate a stratified design for the landscape
    INPUTS:
        mask: (.tif) Binary invalid areas mask of size (imheight, imwidth) showing areas which should not be sampled
        nsp: (integer) Desired number of sample sites
    OUTPUTS:
        xy0: (.npy) A (2, nsp) dimension list of x, y coordinates for the chosen sample sites
    """

    # Initialise empty arrays and lists to save design
    imheight, imwidth = mask.shape
    dist_im = np.ones((imheight, imwidth))
    sites = np.ones((imheight, imwidth))
    mask_aux = copy(mask)
    x_vals = []
    y_vals = []

    for i in range(nsp):

        # Make all elements of EDT map in invalid region 0
        dist_im = dist_im * mask_aux

        # Extract coords of pixels with maximum distance value
        dist_mx = list(zip(*np.where(dist_im == dist_im.max())))

        # Choose one max coord pair at random
        idx = randint(0, len(dist_mx) - 1)
        x, y = dist_mx[idx]

        # Save x and y coords
        x_vals = np.append(x_vals, x)
        y_vals = np.append(y_vals, y)

        # Code chosen site to be zero (a feature pixel) in site array
        sites[x, y] = 0

        # Update the euclidean distance transform
        dist_im = ndimage.distance_transform_edt(sites)

        print('Plotted sample site {}'.format(i+1))

    #xy0 = np.hstack([x_vals, y_vals])
    #return xy0
    return x_vals, y_vals