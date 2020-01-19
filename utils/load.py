from osgeo import gdal
import numpy as np
from scipy import ndimage


def get_file_info(file_path):
    '''
    Function which extracts a geotiff file as numpy array, and saves geographic projection information
    input:
        file_path: (str) Path to the file
    output:
        file_map: (np.array) The extracted map
        nbins: (int) The number of categories in the map
        res: (float) Resolution of the map in meters
        GeoT: The geographic transform used to project the map
        auth_code: The authority code matching the projection
    '''
    file_raw = gdal.Open(file_path)
    prj_info = file_raw.GetProjection()
    GeoT = file_raw.GetGeoTransform()
    res = GeoT[1]
    file_map = file_raw.ReadAsArray()
    nbins = len(np.unique(file_map))
    return file_map, nbins, res, GeoT, prj_info


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
    imheight, imwidth = mask.shape
    mask_update = np.ones((imheight, imwidth))
    # Code the point to mask as zero
    center_pixel = site_df.loc[site_df['sampled']==2]
    x = center_pixel['row'].values; y = center_pixel['col'].values
    mask_update[x,y] = 0
    # Threshold distance transform and add to original mask
    dist_im = ndimage.distance_transform_edt(mask_update)*res
    dist_im[dist_im<radius] = 0; dist_im[dist_im>=radius] = 1;
    mask_inv = 1-mask; mask_new = 1-dist_im*mask_inv
    mask_new_inv = 1-mask_new
    return mask_new, mask_new_inv


