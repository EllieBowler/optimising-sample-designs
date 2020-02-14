import numpy as np
import pandas as pd


def discretize_metric(metric, mask, n_bins):
    """
    Convert continuous metrics to discrete, based on the specified number of bins
    INPUTS:
        metric: (np.array) fragmentation metric map
        mask: (np.array) binary mask showing locations which should not be sampled
        n_bins: (int) number of intervals the range of the metric should be divided into
    OUTPUTS:
        metric_bin: (np.array) the binned fragmentation metric
        ids: (list) the unique id values assigned to each bin
        breaks: (list) the intervals where the range of the metric was split
    """
    imheight, imwidth = metric.shape
    # Mask out invalid areas of metric (numpy masked array function reads one as invalid, so invert mask)
    metric_mask = np.ma.masked_array(metric, mask=(1-mask))
    # Break range of unmasked metric values into 'n_bins' intervals
    hist, breaks = np.histogram(metric_mask.compressed(), bins=n_bins)
    # Each bin a unique integer ID
    ids = np.arange(0, n_bins)
    ones = np.ones((imheight, imwidth))
    metric_bin = np.zeros((imheight, imwidth))
    # Loop through ID's and convert all values in each bin to corresponding id
    for ID in ids:
        # Closed on the lower bound, open on the top
        lower_lim = np.where(ones, metric_mask >= breaks[ID], 0)
        upper_lim = np.where(ones, metric_mask < breaks[ID+1], 0)
        # Make the last interval closed at the upper bound
        if ID == n_bins-1:
            upper_lim = np.where(ones, metric_mask <= breaks[ID+1], 0)
        metric_bin += lower_lim*upper_lim*ID
    return metric_bin, ids, breaks


def build_df(bin_ids):
    """
    Create a data frame showing all combinations of unique metric ids
    INPUTS:
        bin_ids: (list) list of id values for each of the metric maps
    OUTPUTS:
        combo_df: (data frame) data frame of all combinations
    """
    # Create array of all combinations
    id_mesh = np.meshgrid(*bin_ids)
    # Convert to data frame, each row represents a unique combination of the ID's
    combo_df = pd.DataFrame([ids.flatten() for ids in id_mesh]).T
    return combo_df


def bin_metrics(metric_list, mask, bins_list):
    """
    Bin all input metric arrays into discrete ID arrays, and create a data frame of all the
    unique combinations of these IDs
    INPUTS:
        metric_list: (list) list containing each of the input metric maps
        mask: (np.array) binary mask showing locations which should not be sampled
        bins_list: (list) number of bins each metric should be broken into
    OUTPUTS:
        binned_metrics: (list) list of all the binned metrics
        combo_df: (data frame) data frame of all combinations
        bin_breaks: (list) list of break points used to discretize the metrics
    """
    binned_metrics = []
    bin_ids = []
    bin_breaks = []
    # Generate a binned version of all input metric arrays
    for i in range(len(metric_list)):
        metric_bin, ids, breaks = discretize_metric(metric_list[i], mask, bins_list[i])
        binned_metrics.append(metric_bin)  # Save all new (discretized) metric arrays
        bin_ids.append(ids)  # Save the list of all IDs present for each array
        bin_breaks.append(breaks)  # Save the bin breaks for each metric
    # Generate data frame of all combinations of IDs between the input metric arrays
    combo_df = build_df(bin_ids)
    return binned_metrics, combo_df, bin_breaks


def generate_all_layers(binned_metrics, mask, combo_df, nsp):
    """
    Create one-hot masks for each ID and calculate the optimum number of sample sites in each ID
    INPUTS:
        binned_metrics: (list) list of all the binned metrics
        mask: (np.array) binary mask showing locations which should not be sampled
        combo_df: (data frame) data frame of all combinations
        nsp: (int) integer number of sample sites
    OUTPUTS:
        all_layers: (np.array) one-hot masks for each of the unique ids
        id_df: (data frame) reduced version of combo_df, with all empty ids removed
        s_opt: (float) the optimal number of sample sites per id
    """
    imheight, imwidth = mask.shape
    combo_num = len(combo_df)
    # create 3d array to store ID combo layers in
    all_layers = np.zeros((combo_num, imheight, imwidth))
    counts = []
    # Iterate through all unique ID combinations
    for i in range(combo_num):
        im_layer = np.ones((imheight, imwidth))
        for j in range(len(binned_metrics)):
            # Convert selected ID to binary for each metric, and multiply together to see where
            # combinations are in the landscape image
            im_layer = np.where(binned_metrics[j] == combo_df.iloc[i][j], 1, 0) * im_layer
        # Make sure invalid areas are set as zero
        layer_mask = im_layer * mask
        counts.append(np.sum(layer_mask))  # Store the number of pixels in each unique combo layer
        all_layers[i, :, :] = layer_mask  # Save combo Id layer in 3d array
    combo_df['Counts'] = counts
    id_df = combo_df[combo_df.Counts != 0]  # remove empty bins to create ID data frame
    s_opt = np.float(nsp) / len(id_df)  # optimum sample sites in each ID
    id_df = id_df[id_df.Counts >= 10 * np.ceil(s_opt)]  # remove IDs with too few pixels
    s_opt = np.float(nsp) / len(id_df)
    return all_layers, id_df, s_opt


def generate_id_im(all_layers, id_df):
    """
    Create single combined ID array
    INPUTS:
        all_layers: (np.array) one-hot masks for each of the unique ids
        id_df: (data frame) reduced version of combo_df, with all empty ids removed
    OUTPUTS:
        id_im: (np.array) combined id image
        unique_ids: (list) list of unique ids contained in id_im
    """
    imdepth, imheight, imwidth = all_layers.shape
    id_im = np.zeros((imheight, imwidth))
    counter = 0
    unique_ids = []
    for k in id_df.index.values:
        id_im += all_layers[k, :, :] * (counter + 1)
        unique_ids.append(counter + 1)
        counter += 1
    # Save an ID image for adapted uniform designs
    # np.save("{0}/{1}Site_Uniform_IDim".format(savepath, nsp), ID_im)
    return id_im, unique_ids


def upper_lower_suggest(nsp, id_df):
    """
    Calculate upper and lower number of sample sites to meet uniform distribution
    INPUTS:
        all_layers: (np.array) one-hot masks for each of the unique ids
        id_df: (data frame) reduced version of combo_df, with all empty ids removed
    OUTPUTS:
        nsp_lower: (int) lower number of sample sites per id
        nsp_upper: (int) upper number of sample sites per id
    """
    nsp = float(nsp)
    n_bins = len(id_df)
    nsp_lower = np.floor(nsp / n_bins) * n_bins
    nsp_upper = np.ceil(nsp / n_bins) * n_bins
    return nsp_lower.astype(int), nsp_upper.astype(int)


def generate_id_list(unique_ids, s_opt, nsp, id_df):
    """
    Generate a list of ids to sample in the design
    INPUTS:
        unique_ids: (list) list of unique ids contained in id_im
        s_opt: (float) the optimal number of sample sites per id
        nsp: (int) integer number of sample sites
        id_df: (data frame) reduced version of combo_df, with all empty ids removed
    OUTPUTS:
        id_mix: (np.array) list of ids to sample, randomly shuffled
        id_df: (data frame) reduced version of combo_df, with all empty ids removed
    """
    id_rep = np.repeat(unique_ids, np.floor(s_opt))
    diff = nsp - len(id_rep)
    if diff > 0:
        print('difference of {}'.format(diff))
        extra_ids = np.random.choice(unique_ids, diff, replace=False)
        id_rep = np.hstack([id_rep, extra_ids])
    elif diff < 0:
        print('error')
    else:
        print('{} sample sites requested, {} sampled'.format(nsp, len(id_rep)))
    # If nsp is less than the number of IDs (i.e one or less sample per ID),
    # then create a reduced data frame
    if len(id_rep) < len(unique_ids):
        print('creating reduced data frame')
        df_ids = [i - 1 for i in id_rep]
        id_df = id_df.iloc[df_ids, :].copy(deep=True)
    id_df['Freq'] = np.unique(id_rep, return_counts=True)[1]
    id_mix = np.random.permutation(id_rep)
    return id_mix, id_df


def get_sampling_info(df_path):
    # All sites
    site_df = pd.read_csv(df_path)
    nsp = len(site_df)
    unique_IDs = np.unique(site_df.combocode.values)
    # Sampled sites
    sampled_df = site_df.loc[site_df['sampled'] == 1]
    nsampled = len(sampled_df)
    # Unsampled sites
    unsampled_df = site_df.loc[site_df['sampled'] != 1]
    id_mix_unsampled = np.random.choice(unsampled_df.combocode.values, len(unsampled_df), replace=False)
    save_IDs = np.hstack([sampled_df.combocode.values, id_mix_unsampled])
    return sampled_df, nsp, id_mix_unsampled, save_IDs, unique_IDs, nsampled
