import pandas as pd
import numpy as np
from osgeo import osr, ogr
import time
import os


def lat_long_convert(x, y, prj_info, geo_t):
    """
    Convert x, y coordinates to longitude and latitude, using projection info contained in the geo-tiff
    INPUTS:
        x: (list) x coordinates of sample sites
        y: (list) y coordinates of sample sites
        prj_info: (string) projection information extracted from geo-tiff
        geo_t: (list) geographic transformation values extracted from geo-tiff
    OUTPUTS:
        long: (list) longitude values of sample sites
        lat: (list) latitude values of sample sites
    """
    # Project row and column (will be for bottom left corner)
    x_proj = x * geo_t[1] + geo_t[0]
    y_proj = y * geo_t[5] + geo_t[3]

    # Shift from bottom left to centre of the pixel
    x_proj += geo_t[1] / 2.0
    y_proj += geo_t[5] / 2.0

    xy_proj = np.stack((x_proj, y_proj), axis=-1)

    # Make spatial coordinate system
    srs = osr.SpatialReference()
    if srs.ImportFromWkt(prj_info) != 0:
        print("Error: cannot import projection '%s'" % prj_info)
        sys.exit(1)

    srs_lat_long = srs.CloneGeogCS()
    ct = osr.CoordinateTransformation(srs, srs_lat_long)
    long, lat, height = list(zip(*ct.TransformPoints(xy_proj)))
    return long, lat


def save_as_shp(x, y, geo_t, out_filename):
    """
    Export sample site locations to shape file, to be read into software like ArcMap
    INPUTS:
        x: (list) x coordinates of sample sites
        y: (list) y coordinates of sample sites
        geo_t: (list) geographic transformation values extracted from geo-tiff
        out_filename: (str) path and name of the output shape file
    OUTPUTS:
        Saves .shp file in the directory specified by out_filename
    """
    # Create the ESRI shape file
    driver = ogr.GetDriverByName('ESRI Shapefile')
    ds = driver.CreateDataSource(out_filename)

    layer = ds.CreateLayer('', None, ogr.wkbPoint)
    for i in range(len(x)):
        feature = ogr.Feature(layer.GetLayerDefn())

        # Project row and column (will be for bottom left corner)
        x_proj = y[i] * geo_t[1] + geo_t[0]
        y_proj = x[i] * geo_t[5] + geo_t[3]

        # Shift from bottom left to centre of the pixel
        x_proj += geo_t[1] / 2.0
        y_proj += geo_t[5] / 2.0

        # Add each point to new geometry
        point = ogr.Geometry(ogr.wkbPoint)
        point.AddPoint(x_proj, y_proj)
        feature.SetGeometry(point)
        layer.CreateFeature(feature)
        feature.Destroy()

    # Delete driver once finished
    ds.Destroy()
    return


def save_stratified(x, y, prj_info, geo_t, save_path, sampled_csv=None):
    """
    Function to output final sample design to .csv and ESRI .shp file
    INPUTS:
        x: (list) x coordinates of sample sites
        y: (list) y coordinates of sample sites
        prj_info: (string) projection information extracted from geo-tiff
        geo_t: (list) geographic transformation values extracted from geo-tiff
        save_path: (str) path specifying where to save the .csv and .shp files
        sampled_csv: (data frame) only entered if updating a design, else None
    OUTPUTS:
        Saves .csv in the directory specified by save_path
    """
    # Generate unique time stamp to avoid overwriting results
    ts = time.gmtime()
    ts = time.strftime("%Y_%m_%d_%H%M%S", ts)

    # Convert from row/col to projected
    long, lat = lat_long_convert(x, y, prj_info, geo_t)

    # Make data frame using pandas
    result = pd.DataFrame()
    result['longitude'] = long
    result['latitude'] = lat
    result['row'] = x
    result['col'] = y
    result['sampled'] = 0
    csv_filename = '{}_{}site_strat'.format(ts, len(x))

    # For adapted designs add info to the sampled column
    if sampled_csv is not None:
        num_sampled = sum(sampled_csv.sampled)
        result['sampled'] = [1] * num_sampled + [0] * (len(x) - num_sampled)
        csv_filename = '{}_{}site_strat_adapted'.format(ts, len(x))

    # Write to csv and shape files
    result.index += 1
    result.to_csv('{}/{}.csv'.format(save_path, csv_filename), index_label='site')
    save_as_shp(x, y, geo_t, '{}/{}.shp'.format(save_path, csv_filename))
    print('Design saved as .csv and .shp in {} directory \nFile name: {}'.format(save_path, csv_filename))
    return


def save_uniform(x, y, id_mix, id_df, id_im, prj_info, geo_t, save_path, sampled_csv=None):
    """
    Function to output final sample design to .csv and ESRI .shp file
    INPUTS:
        x: (list) x coordinates of sample sites
        y: (list) y coordinates of sample sites
        prj_info: (string) projection information extracted from geo-tiff
        geo_t: (list) geographic transformation values extracted from geo-tiff
        save_path: (str) path specifying where to save the .csv and .shp files
        sampled_csv: (data frame) only entered if updating a design, else None
    OUTPUTS:
        Saves .csv in the directory specified by save_path
    """
    # Generate unique time stamp to avoid overwriting results
    ts = time.gmtime()
    ts = time.strftime("%y_%m_%d_%H%M%S", ts)

    if not os.path.exists('{}/{}'.format(save_path, ts)):
        os.makedirs('{}/{}'.format(save_path, ts))

    # Convert from row/col to projected
    long, lat = lat_long_convert(x, y, prj_info, geo_t)

    # Make data frame using pandas
    result = pd.DataFrame()
    result['longitude'] = long
    result['latitude'] = lat
    result['row'] = x
    result['col'] = y
    result['sampled'] = 0
    result['ID'] = id_mix
    csv_filename = '{}site_unif'.format(len(x))

    # For adapted designs add info to the sampled column
    if sampled_csv is not None:
        num_sampled = sum(sampled_csv.sampled)
        result['sampled'] = [1] * num_sampled + [0] * (len(x) - num_sampled)
        csv_filename = '{}site_unif_adapted'.format(len(x))

    # Merge with id_df to store individual metric id values
    result = pd.merge(result, id_df)

    # Write to csv and shape files
    result.index += 1
    result.to_csv('{}/{}/{}.csv'.format(save_path, ts, csv_filename), index_label='site')
    save_as_shp(x, y, geo_t, '{}/{}/{}.shp'.format(save_path, ts, csv_filename))
    np.savez('{}/{}/{}.npz'.format(save_path, ts, csv_filename))
    print('Design saved as .csv and .shp in {}/{} directory \nFile name: {}'.format(save_path, ts, csv_filename))
    print('Also saving id_im as {}.npz, which is used to adapt the uniform design'.format(csv_filename))
    return