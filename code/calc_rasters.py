#hack to use correct python version
import sys
sys.path.reverse()

import gdal
from gdalconst import *

import numpy as np
import struct

# helper functions
def fix_aspects(gradx,grady,slope):
    if slope == 0:
        return 0
    else:
        if gradx < 0:
            return np.arccos(grady/slope)*180/np.pi
        else:
            return 360 - np.arccos(grady/slope)*180/np.pi

def fix_slopes(slope):
    if slope > 500.:
        return 0
    else:
        return slope

# vectorize these for code readability later on
vector_fix_aspects = np.vectorize(fix_aspects, otypes=[np.float])
vector_fix_slopes = np.vectorize(fix_slopes, otypes=[np.float])

# open the raster and store some information about it
def gen_files(path, s_path, a_path,name,ext):
    # open provided file
    dataset = gdal.Open(path+name+ext, GA_ReadOnly)
    # get driver
    gtiff = gdal.GetDriverByName('GTiff')
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
    dem_data = data_1D.reshape(ysize,xsize)
    gradient_data = np.gradient(dem_data,90.)
    magnitude_data = vector_fix_slopes(np.sqrt((gradient_data[0]**2) + (gradient_data[1]**2)))
    slope_data = np.arctan(magnitude_data)
    aspect_data = vector_fix_aspects(gradient_data[0], gradient_data[1], magnitude_data)

    # Generate slope raster
    slope_out = gtiff.Create(s_path+name+'_s'+ext, xsize, ysize, 1, gdal.GDT_Float32)
    slope_out.SetProjection(projectionfrom)
    slope_out.SetGeoTransform(geotransform)
    slope_out.GetRasterBand(1).WriteArray(slope_data)
    slope_out.GetRasterBand(1).FlushCache()

    # Generate aspect raster
    aspect_out = gtiff.Create(a_path+name+'_a'+ext, xsize, ysize, 1, gdal.GDT_Float32)
    aspect_out.SetProjection(projectionfrom)
    aspect_out.SetGeoTransform(geotransform)
    aspect_out.GetRasterBand(1).WriteArray(aspect_data)
    aspect_out.GetRasterBand(1).FlushCache()

    slope_out = None
    aspect_out = None
    dataset = None

#load the 10m DEM raster files
demPath = "../data/GIS/tifs/dem/"
slopePath = "../data/GIS/tifs/slope/"
aspectPath = "../data/GIS/tifs/aspect/"
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
    gen_files(demPath,slopePath,aspectPath,file_n,fileExt)

#####
