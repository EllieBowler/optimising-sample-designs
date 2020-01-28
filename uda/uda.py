import numpy as np
from random import randint
from scipy import ndimage


def generate_uniform_design(id_mix, unique_IDs, store_masks):

    """Generate a uniform design.
    Inputs: id_mix - A list where each ID is repeated by the number of sample sites
                    it requires for a normal distribution
            unique_IDs - A list of all the unique IDs
            store_masks - A 3d array which contains binary maps for each ID, with
                    0=pixel not in ID/ 1=pixel is in ID.
    Outputs: Points in uniform design in row and column format"""

    imdepth, imheight, imwidth = store_masks.shape
    dist_im = np.ones((imheight, imwidth))
    sites = np.ones((imheight, imwidth))
    x_vals = []
    y_vals = []
    loop_count = 0

    for i in id_mix:

        loop_count += 1
        print('Plotting site {}, id number {}'.format(loop_count, i))

        maskID = np.where(ID_im == i, 1, 0)
        layer = maskID * dist_im

        # Select binary map relating to selected ID
        # maskID = unique_IDs.index(i)
        # Mask out any regions of EDT not in ID
        # layer = store_masks[maskID, :, :] * dist_im

        # Extract coords of pixels with maximum distance value and choose one at random
        # dist_mx = zip(*np.where(layer == layer.max()))
        dist_mx = list(zip(*np.where(layer == layer.max())))
        idx = randint(0, len(dist_mx) - 1)
        x, y = dist_mx[idx]

        # Save coordinates
        x_vals = np.append(x_vals, x)
        y_vals = np.append(y_vals, y)

        # Add selected site to sites array as 0 (feature pixel)
        sites[x, y] = 0

        # Compute EDT from all placed sites
        dist_im = ndimage.distance_transform_edt(sites)

    print('Uniform sample design complete!')
    # xy0 = np.hstack([x_vals, y_vals])
    return x_vals, y_vals