####################
# Phil Ngo
# Lots of help from this blog!
# http://geoexamples.blogspot.com/2012/02/raster-classification-with-gdal-python.html
####################
import sys
sys.path.reverse()

from PyQt4.QtCore import *
from qgis.core import *
import qgis.utils

import gdal
from gdalconst import *

import numpy as np
import struct

import pdb

# helper functions

# get aspect
def deg_from_N(gradx,grady,slope):
    if slope == 0:
        return 0
    else:
        if gradx < 0:
            return np.arccos(grady/slope)*180/np.pi
        else:
            return 360 - np.arccos(grady/slope)*180/np.pi

# vectorize it for readability
vector_deg_from_N = np.vectorize(deg_from_N, otypes=[np.float])

def make_slopes_better(slope):
    if slope > 500.:
        return 0
    else:
        return slope

# vectorize it for readability
vector_make_slopes_better = np.vectorize(make_slopes_better, otypes=[np.float])

#load the 10m DEM raster files
demPath = "../data/GIS/tifs/dem/"
slopePath = "../data/GIS/tifs/slope/"
aspectPath = "../data/GIS/tifs/aspect/"
fileName = "40111b4"
fileExt = ".tif"

# QGIS stuff
#fileInfo = QFileInfo(fileName)
#baseName = fileInfo.baseName()
#rlayer = QgsRasterLayer(fileName, baseName)
#if not rlayer.isValid():
#    print "Layer failed to load!"

# open the raster and store some information about it
dataset = gdal.Open(demPath+fileName+fileExt, GA_ReadOnly)
projectionfrom = dataset.GetProjection()
geotransform = dataset.GetGeoTransform()
band = dataset.GetRasterBand(1)
xsize, ysize = band.XSize, band.YSize
minmax = band.ComputeRasterMinMax()
datatype = band.DataType
values = band.ReadRaster( 0, 0, xsize, ysize, xsize, ysize, datatype )

# Conversion between GDAL types and python pack types
# -- http://geoexamples.blogspot.com/2012/02/raster-classification-with-gdal-python.html
data_types ={'Byte':'B','UInt16':'H','Int16':'h','UInt32':'I','Int32':'i','Float32':'f','Float64':'d'}
data_tuple = struct.unpack(data_types[gdal.GetDataTypeName(band.DataType)]*xsize*ysize,values)

# convert the tuple into into a numpy array and calculate some useful data
data_1D = np.asarray(data_tuple)
dem_data = data_1D.reshape(ysize,xsize)
gradient_data = np.gradient(dem_data,10.)
#slope_data = np.sqrt((gradient_data[0]**2) + (gradient_data[1]**2))
slope_data = vector_make_slopes_better(np.sqrt((gradient_data[0]**2) + (gradient_data[1]**2)))
aspect_data = vector_deg_from_N(gradient_data[0], gradient_data[1], slope_data)



#cols = 10
#rows = 20

#a = np.zeros((10,20))

#dst_filename = 'test.tif'
#format = 'GTiff'
#driver = gdal.GetDriverByName(format)

#dst_ds = driver.Create(dst_filename, cols, rows, 1, gdal.GDT_Byte)

#dst_ds.GetRasterBand(1).WriteArray(a)
#output raster of slope data
gtiff = gdal.GetDriverByName('GTiff')

aspect_out = gtiff.Create(aspectPath+fileName+'_a'+fileExt, xsize, ysize, 1, gdal.GDT_Float32)
aspect_out.SetProjection(projectionfrom)
aspect_out.SetGeoTransform(geotransform)
aspect_out.GetRasterBand(1).WriteArray(aspect_data)
aspect_out.GetRasterBand(1).FlushCache()
aspect_out = None


slope_out = gtiff.Create(slopePath+fileName+'_s'+fileExt, xsize, ysize, 1, gdal.GDT_Float32)
slope_out.SetProjection(projectionfrom)
slope_out.SetGeoTransform(geotransform)
slope_out.GetRasterBand(1).WriteArray(slope_data)
slope_out.GetRasterBand(1).FlushCache()
slope_out = None
#output raster of aspect data
#dst_ds.SetGeoTransform( [ 444720, 30, 0, 3751320, 0, -30 ] )

#srs = osr.SpatialReference()
#srs.SetUTM( 11, 1 )
#srs.SetWellKnownGeogCS( 'NAD27' )
#dst_ds.SetProjection( srs.ExportToWkt() )

#raster = numpy.zeros( (512, 512), dtype=numpy.uint8 )
#dst_ds.GetRasterBand(1).WriteArray( raster )

# Once we're done, close properly the dataset
#dst_ds = None

dataset = None
