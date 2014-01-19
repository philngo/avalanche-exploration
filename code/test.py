import sys
sys.path.reverse()
import numpy as np
import gdal

cols = 50
rows = 70
offset = 0

dst_filename = 'test.tif'
format = 'GTiff'
driver = gdal.GetDriverByName(format)

dst_ds = driver.Create(dst_filename, cols, rows, 1, gdal.GDT_Byte)

for i in range(10):
    # generate random integers from 1 to 10
    a = np.random.random_integers(1, 10, size=(offset, cols))
    # write data to band 1
    dst_ds.GetRasterBand(1).WriteArray(a, 0, offset * i)

dst_ds = None
