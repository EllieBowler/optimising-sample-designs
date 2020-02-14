import numpy as np
from random import randint
from scipy import ndimage


def generate_uniform_design(id_mix, id_im):
    """
    Main function for generating a uniform design.
    Places site evenly within the range of the input metrics, while also spacing them as evenly as possible spatially.
    INPUTS:
        id_mix: (list) list of metric id values to be sampled
        id_im: (np.array) distribution of all metric id values in the study landscape
    OUTPUTS:
        x_vals: (list) x coordinates of sample sites
        y_vals: (list) y coordinates of sample sites
    """

    # Initialise empty arrays and lists to save design
    imheight, imwidth = id_im.shape
    dist_im = np.ones((imheight, imwidth))
    sites = np.ones((imheight, imwidth))
    x_vals = []
    y_vals = []
    loop_count = 1

    for i in id_mix:
        print('Plotting site {}, id number {}'.format(loop_count, i))

        # Select binary map relating to selected ID
        mask_id = np.where(id_im == i, 1, 0)

        # Mask out any regions of EDT not in ID
        layer = mask_id * dist_im

        # Extract coordinates of pixels with maximum distance value
        dist_mx = list(zip(*np.where(layer == layer.max())))

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

        loop_count += 1

    print('Uniform sample design complete!')
    return x_vals, y_vals
