# import modules
import sys
sys.path.reverse()

import gdal
from gdalconst import *

import numpy as np
import struct

import pdb


# Helper functions
def open_tif(path, name, ext):
    # open provided file
    dataset = gdal.Open(path+name+ext, GA_ReadOnly)
    # save some metadata for output
    projectionfrom = dataset.GetProjection()
    geotransform = dataset.GetGeoTransform()
    band = dataset.GetRasterBand(1)
    xsize, ysize = band.XSize, band.YSize
    datatype = band.DataType
    values = band.ReadRaster( 0, 0, xsize, ysize, xsize, ysize, datatype )

    # Conversion between GDAL types and python pack types
    data_types ={'Byte':'B','UInt16':'H','Int16':'h','UInt32':'I','Int32':'i','Float32':'f','Float64':'d'}
    data_tuple = struct.unpack(data_types[gdal.GetDataTypeName(band.DataType)]*xsize*ysize,values)

    # convert the tuple into into a numpy array and calculate some useful data
    data_1D = np.asarray(data_tuple)
    data_arr = data_1D.reshape(ysize,xsize)
    return data_arr, projectionfrom, geotransform

def open_esa_tifs(e_path,s_path,a_path,name,ext):
    dem_data, dem_projection, dem_geotransform = open_tif(e_path, name, ext)
    slp_data, slp_projection, slp_geotransform = open_tif(s_path,name+'_s',ext)
    asp_data, asp_projection, asp_geotransform = open_tif(a_path,name+'_a',ext)
    return [dem_data,slp_data,asp_data], \
           [dem_projection, slp_projection, asp_projection], \
           [dem_geotransform, slp_geotransform, asp_geotransform]


def predictor(elev,slope,aspect):
    # slope angles between 20 and 45 are the worst
    if slope > np.pi/9 and slope < np.pi/4:
        slope_danger = 1 - (abs ((np.pi/5 - slope)) / (np.pi/4 - np.pi/9))
    else:
        slope_danger = 0

    # higher elevation is the worst
    # logistic function centered at 2750
    if elev > 3200:
        elev_danger = 1
    elif elev < 2300:
        elev_danger = 0
    else:
        elev_danger = 1/(1 + np.exp( (2750 - elev)/120))

    # North facing slopes are the worst
    if abs(270 - aspect) < 90:
        aspect_danger = 1 - abs(270 - aspect)/180
    else:
        aspect_danger = .5

    return slope_danger * aspect_danger * elev_danger


vector_predictor = np.vectorize(predictor, otypes=[np.float])

def gen_prediction(path, name, ext):
    # get model data
    terrain_data, projections, geotransforms = \
        open_esa_tifs("../data/GIS/tifs/dem/",\
                      "../data/GIS/tifs/slope/",\
                      "../data/GIS/tifs/aspect/",\
                      name,ext)
    # write output file
    gtiff = gdal.GetDriverByName('GTiff')
    pred = gtiff.Create(path + name + "_p" + ext, terrain_data[0].shape[1], terrain_data[0].shape[0], 1, gdal.GDT_Float32)
    pred.SetProjection(projections[0])
    pred.SetGeoTransform(geotransforms[0])
    pred.GetRasterBand(1).WriteArray(vector_predictor(terrain_data[0],terrain_data[1],terrain_data[2]))
    pred.GetRasterBand(1).FlushCache()

predictionPath = "../predictions/terrain_only/"
fileNames = ["o11140"]
'''
fileNames = ["40111b4","40111b5","40111b6",\
             "40111c4","40111c5","40111c6",\
             "40111d4","40111d5","40111d6","40111d7",\
             "40111e4","40111e5","40111e6","40111e7",\
             "40111f4","40111f5","40111f6","40111f7",\
             "40111g4","40111g5","40111g6","40111g7","40111g8",\
             "o11140"]

'''
fileExt = ".tif"

for file_n in fileNames:
    gen_prediction(predictionPath,file_n,fileExt)

