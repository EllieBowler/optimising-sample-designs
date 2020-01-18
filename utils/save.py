import pyproj as pyproj
import pandas as pd
import numpy as np


def get_site_values(result, x, y, immetrics, binned_metrics):
    """
    Extract metric values at the sample site locations.
    :param result:
    :param x:
    :param y:
    :param immetrics:
    :param binned_metrics:
    :return:
    """

def LongLatConvert(x, y, GeoT, auth_code):
    """"
    Convert x, y pixel coords (locations in numpy array), to long/lat
    using geotiff info taken from input file
    INPUTS:
        x:
        y:
        GeoT:
        auth_code:
    OUTPUTS:
        longlat:
    """
    x_proj = x * GeoT[1] + GeoT[0] + (GeoT[1] / 2)
    y_proj = y * GeoT[5] + GeoT[3] + (GeoT[5] / 2)
    p1 = pyproj.Proj(init='EPSG:'+auth_code)
    longlat = p1(x_proj, y_proj, inverse=True)
    return longlat


def save_stratified(x, y, GeoT, auth_code, savepath, nsampled=0, updated=''):
    """Convert sites to lists of geographic coordinates and save as csv files"""
    nsp = len(x)
    # Convert from row/col to projected
    longlat = LongLatConvert(x, y, GeoT, auth_code)
    # Reformat and save to csv
    result = pd.DataFrame(list(zip(*longlat)), columns = ['longitude','latitude'])
    result.index += 1; result['row'] = x; result['col'] = y
    result['sampled'] = np.hstack(([1]*nsampled, [0]*(nsp-nsampled)))
    result.to_csv('{0}/{1}Site_Stratified_Design{2}.csv'.format(savepath, nsp, updated), index_label='site')
    return