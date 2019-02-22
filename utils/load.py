from osgeo import gdal, osr
import numpy as np

def get_file_info(file_path):
    """"
    Extract array and geo-information from satellite image of study location.
    Should be CATEGORICAL (e.g habitat/non-habitat map).
    INPUTS:
        file_path: (string) Relative path to .tif file
        * Note file should be a geotiff with projection details etc
    OUTPUTS:
        file_map: (.npy array) 2D numpy array of study site
        nbins: (integer) The number of unique categories in the map image
        res: (integer) The resolution of the image (e.g area represented by each pixel
        GeoT: GeoTransform information, for reprojecting site locations to long/lat
    """

    file_raw = gdal.Open(file_path)
    prj = file_raw.GetProjection(); srs = osr.SpatialReference(wkt=prj)
    auth_code = srs.GetAuthorityCode(None)
    GeoT = file_raw.GetGeoTransform(); res = GeoT[1]
    file_map = file_raw.ReadAsArray()
    nbins = len(np.unique(file_map))

    return file_map, nbins, res, GeoT, auth_code

def extract_raster(file_path):
    """
    Extract array from satellite image of study location.
    *Same as get_file_info but without geo-information
    INPUTS:
        file_path: (string) Relative path to .tif file
    OUTPUTS:
        file_map: (.npy array) 2D numpy array of study site
    """
    file_raw = gdal.Open(tif_path)
    file_map = tif_raw.ReadAsArray()
    return file_map



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
    mask_new_inv = 1- mask_new
    return mask_new, mask_new_inv


