from matplotlib import pyplot as plt
import numpy as np


def plot_uniform(id_im, mask, x, y):
    """
    Plot initial uniform design
    INPUTS:
        id_im: (.npy array) map showing distribution of ids in the landscape
        mask: (.npy array) binary mask showing locations which should not be sampled
        x: (list) x coordinates of sample sites
        y: (list) y coordinates of sample sites
    OUTPUTS:
        Creates a pop up for the design, should be closed manually
    """
    print('Close plot to save results and continue running the code...')
    id_im_msk = np.ma.masked_array(id_im, mask=(1-mask))
    plt.imshow(id_im_msk)
    plt.scatter(y, x, c='black', marker='x', linewidth=2)
    plt.axis('off')
    plt.title('Uniform design with {} sample sites'.format(len(x)))
    plt.show()
    return


def plot_stratified(mask, x, y):
    """
    Plot initial stratified design
    INPUTS:
        mask: (.npy array) binary mask showing locations which should not be sampled
        x: (list) x coordinates of sample sites
        y: (list) y coordinates of sample sites
    OUTPUTS:
        Creates a pop up for the design, should be closed manually
    """
    print('Close plot to save results and continue running the code...')
    plt.figure(figsize=(7, 9))
    plt.imshow(mask, cmap=plt.cm.get_cmap('Accent_r', 2))
    plt.title('{} design with {} sample sites'.format('Stratified', len(x)))
    plt.axis('off')
    cbar = plt.colorbar(fraction=0.02, orientation='horizontal', pad=0.01)
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(['0: Invalid', '1: Valid'])
    plt.scatter(y, x, c='black', marker='x', linewidth=1.5, s=70)
    plt.show()
    return


def plot_adapted_stratified(mask, x, y, sampled_csv):
    """
    Plot updated stratified design
    INPUTS:
        mask: (.npy array) binary mask showing locations which should not be sampled
        x: (list) x coordinates of sample sites
        y: (list) y coordinates of sample sites
        sampled_csv: (data frame) data frame containing sample site information
    OUTPUTS:
        Creates a pop up for the design, should be closed manually
    """
    print('Close plot to save results and continue running the code...')
    plt.figure(figsize=(7, 9))
    plt.imshow(mask, cmap=plt.cm.get_cmap('Accent_r', 2))
    plt.title('{} design with {} sample sites'.format('Adapted Stratified', len(x)))
    plt.axis('off')
    cbar = plt.colorbar(fraction=0.02, orientation='horizontal', pad=0.01)
    cbar.set_ticks([0, 1])
    cbar.set_ticklabels(['0: Invalid', '1: Valid'])
    num_sampled = sum(sampled_csv.sampled)
    plt.scatter(y[:num_sampled], x[:num_sampled], c='black', marker='x', linewidth=1.5, s=70, label='Sampled')
    plt.scatter(y[num_sampled:], x[num_sampled:], c='red', marker='x', linewidth=1.5, s=70, label='Shifted')
    plt.legend(loc=(0.95, 0.5))
    plt.show()
    return

