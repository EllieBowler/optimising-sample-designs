import numpy as np
from random import randint
from scipy import ndimage
from copy import copy


def generate_stratified_design(mask, nsp):
    """
    Main function for generating a stratified design.
    Places sites iteratively at the maximum distance apart, spacing them evenly in the landscape.
    INPUTS:
        mask: (.npy array) The invalid areas mask
        nsp: (int) Number of sample sites in design
    OUTPUTS:
        x_vals: (list) x coordinates of sample sites
        y_vals: (list) y coordinates of sample sites
    """

    # Initialise empty arrays and lists to save design
    imheight, imwidth = mask.shape
    dist_im = np.ones((imheight, imwidth))
    sites = np.ones((imheight, imwidth))
    mask_aux = copy(mask)
    x_vals = []
    y_vals = []

    for i in range(nsp):
        print('Plotting site {}'.format(i + 1))

        # Make all elements of EDT map in invalid region 0
        dist_im = dist_im * mask_aux

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

        # Update the euclidean distance transform
        dist_im = ndimage.distance_transform_edt(sites)

    print('Stratified sample design complete!')
    return x_vals, y_vals
