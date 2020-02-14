import numpy as np
from random import randint
from scipy import ndimage
from copy import copy


def update_uniform_design(mask, id_mix, id_im, sampled_csv):
    """
    Main function for updating an existing or partially completed uniform design, when certain sites are inaccessible.
    Places site evenly within the range of the input metrics, while also spacing them as evenly as possible spatially.
    INPUTS:]
        mask: (np.array) updated invalid areas mask showing new inaccessible locations
        id_mix: (list) list of metric id values to be sampled
        id_im: (np.array) distribution of all metric id values in the study landscape
        sampled_csv: (data frame) Tagged data frame output by the original uniform design
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

    imheight, imwidth = id_im.shape
    sites = np.ones((imheight, imwidth))

    sampled_x = sampled_df['row'].values.astype(int)
    sampled_y = sampled_df['col'].values.astype(int)
    sites[sampled_x, sampled_y] = 0
    mask_aux = copy(mask)
    x_vals = [sampled_x]
    y_vals = [sampled_y]

    # Generate EDT image of all sampled/selected sites
    dist_im = ndimage.distance_transform_edt(sites)

    loop_count = 1

    for i in id_mix:
        print('Plotting site {} of {}'.format(loop_count, nsp - n_sampled))

        # Select binary map relating to selected ID
        mask_id = np.where(id_im == i, 1, 0)

        # Mask out any regions of EDT not in ID
        layer = mask_id * dist_im * mask_aux

        # Extract coordinates of pixels with maximum distance value
        dist_mx = list(zip(*np.where(layer == layer.max())))

        # Choose one max coord pair at random
        idx = randint(0, len(dist_mx) - 1)
        x, y = dist_mx[idx]

        # Save coordinates
        x_vals = np.append(x_vals, x)
        y_vals = np.append(y_vals, y)

        # Code chosen site to be zero in site array
        sites[x, y] = 0

        # Update the euclidean distance transform
        dist_im = ndimage.distance_transform_edt(sites)

        loop_count += 1

    print('Adapted uniform design complete!')
    return x_vals, y_vals
