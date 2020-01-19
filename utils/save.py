import pandas as pd
import numpy as np
from osgeo import osr, ogr
import time


def longlat_convert(x, y, prj_info, GeoT):
    # Project row and column (will be for bottom left corner)
    x_proj = x * GeoT[1] + GeoT[0]
    y_proj = y * GeoT[5] + GeoT[3]

    # Shift from bottom left to centre of the pixel
    x_proj += GeoT[1] / 2.0
    y_proj += GeoT[5] / 2.0

    xy_proj = np.stack((x_proj, y_proj), axis=-1)

    # Make spatial coordinate system
    srs = osr.SpatialReference()
    if srs.ImportFromWkt(prj_info) != 0:
        print("Error: cannot import projection '%s'" % prj_info)
        sys.exit(1)

    srsLatLong = srs.CloneGeogCS()
    ct = osr.CoordinateTransformation(srs, srsLatLong)
    long, lat, height = list(zip(*ct.TransformPoints(xy_proj)))
    return long, lat


def save_coords_as_shp(x, y, GeoT, out_filename):
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(out_filename)

    layer = ds.CreateLayer('', None, ogr.wkbPoint)
    for i in range(len(x)):
        feature = ogr.Feature(layer.GetLayerDefn())

        # Project row and column (will be for bottom left corner)
        x_proj = y[i] * GeoT[1] + GeoT[0]
        y_proj = x[i] * GeoT[5] + GeoT[3]

        # Shift from bottom left to centre of the pixel
        x_proj += GeoT[1] / 2.0
        y_proj += GeoT[5] / 2.0

        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(x_proj, y_proj)
        feature.SetGeometry(point)
        layer.CreateFeature(feature)
        feature.Destroy()

    ds.Destroy()
    return


def save_stratified(x, y, prj_info, GeoT, save_path, nsampled=0, updated=''):
    """Convert sites to lists of geographic coordinates and save as csv files"""
    ts = time.gmtime()
    ts = time.strftime("%Y_%m_%d_%H%M%S", ts)
    # Convert from row/col to projected
    long, lat = longlat_convert(x, y, prj_info, GeoT)
    result = pd.DataFrame()
    result['longitude'] = long
    result['latitude'] = lat
    result['row'] = x
    result['col'] = y
    result['sampled'] = 0
    csv_filename = '{}_{}site_strat.csv'.format(ts, len(x))
    result.index += 1
    result.to_csv('{}/{}'.format(save_path, csv_filename), index_label='site')
    print('Design saved as csv in {} directory \nFile name: {}'.format(save_path, csv_filename))
    # Reformat and save to csv
    # result = pd.DataFrame(list(zip(*longlat)), columns = ['longitude','latitude'])
    # result.index += 1; result['row'] = x; result['col'] = y
    # result['sampled'] = np.hstack(([1]*nsampled, [0]*(nsp-nsampled)))
    # result.to_csv('{0}/{1}Site_Stratified_Design{2}.csv'.format(savepath, nsp, updated), index_label='site')
    return
