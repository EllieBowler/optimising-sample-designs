from osgeo import gdal
import numpy as np
from scipy import ndimage


def get_file_info(file_path):
    """
    Function which extracts a geo tiff file as numpy array, and saves geographic projection information
    INPUTS:
        file_path: (str) Path to the file
    OUTPUTS:
        file_map: (np.array) The extracted map
        n_bins: (int) The number of categories in the map
        res: (float) Resolution of the map in meters
        geo_t: (list) The geographic transform used to project the map
    """
    file_raw = gdal.Open(file_path)
    prj_info = file_raw.GetProjection()
    geo_t = file_raw.GetGeoTransform()
    res = geo_t[1]
    file_map = file_raw.ReadAsArray()
    n_bins = len(np.unique(file_map))
    return file_map, n_bins, res, geo_t, prj_info


def extract_raster(tif_path):
    """
    Extract array from satellite image of study location.
    *Same as get_file_info but without geo-information
    INPUTS:
        file_path: (string) Relative path to .tif file
    OUTPUTS:
        file_map: (.npy array) 2D numpy array of study site
    """
    tif_raw = gdal.Open(tif_path)
    return tif_raw.ReadAsArray()


def update_mask(site_df, mask, radius, res):
    """
    Update invalid areas mask by excluding a radius around specified sites
    INPUTS:
        site_df: (panda dataframe) Dataframe containing sample site info and tagged sites
        mask: (.npy array) The original invalid areas mask
        radius: (float) Radius to exclude around tagged sites in metres
        res: (float) Resolution of the satellite image in metres
    OUTPUTS:
        mask_update: (.npy array) Updated mask showing new inaccessible areas
    """
    # Create array same dimensions as input mask
    imheight, imwidth = mask.shape
    new_mask = np.ones((imheight, imwidth))

    # Set the point to mask as a zero
    center_pixel = site_df.loc[site_df['sampled'] == 2]
    x = center_pixel['row'].values.astype(int)
    y = center_pixel['col'].values.astype(int)
    new_mask[x, y] = 0

    # Threshold distance transform and add to original mask
    dist_im = ndimage.distance_transform_edt(new_mask) * res
    dist_im[dist_im < radius] = 0
    dist_im[dist_im >= radius] = 1

    mask_update = dist_im * mask

    return mask_update
