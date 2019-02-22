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


def store_layers(ID_im, mask_inv, unique_IDs):
    imheight, imwidth = mask_inv.shape
    store_masks = np.ones((len(unique_IDs), imheight, imwidth))
    ones = np.ones((imheight, imwidth))
    i = 0
    for ID in unique_IDs:
        store_masks[i, :, :] = np.where(ones, ID_im == ID, 0) * mask_inv
        i += 1
    return store_masks


def update_uniform_design(self, sampled_df, id_mix, store_masks, option):
    """Update existing uniform design when site is inaccessible.
    Inputs: id_mix - A list where each ID is repeated by the number of sample sites
                    it requires for a normal distribution
            unique_IDs - A list of all the unique IDs
            store_masks - A 3d array which contains binary maps for each ID, with
                    0=pixel not in ID/ 1=pixel is in ID.
    Outputs: Points in uniform design in row and column format"""

    sampled_x = sampled_df['row'].values
    sampled_y = sampled_df['col'].values

    imdepth, imheight, imwidth = store_masks.shape
    dist_im = np.ones((imheight, imwidth))
    sites = np.ones((imheight, imwidth))

    sites[sampled_x, sampled_y] = 0
    x_vals = [sampled_x]
    y_vals = [sampled_y]

    loop_count = 0

    for i in id_mix:

        if option == 1:
            self.stat1.set("Computing...{}%".format(np.round(float(loop_count) / len(id_mix) * 100, decimals=0)))
        elif option == 2:
            self.stat2.set("Computing...{}%".format(np.round(float(loop_count) / len(id_mix) * 100, decimals=0)))
        app.update_idletasks()

        # Calculate distance image of already placed sites
        dist_im = ndimage.distance_transform_edt(sites)

        # Mask out any regions of EDT not in ID
        layer = store_masks[i - 1, :, :] * dist_im

        # Extract coords of pixels with maximum distance value and choose one at random
        dist_mx = zip(*np.where(layer == layer.max()))
        idx = randint(0, len(dist_mx) - 1)
        x, y = dist_mx[idx]

        # Save coordinates
        x_vals = np.append(x_vals, x)
        y_vals = np.append(y_vals, y)

        # Add selected site to sites array as 0 (feature pixel)
        sites[x, y] = 0

        loop_count += 1

    xy0 = np.hstack([x_vals, y_vals])
    return xy0
