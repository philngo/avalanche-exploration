import csv
import pdb
import matplotlib.pyplot as plt
import pylab
import numpy as np
from datetime import *
import time
import pickle

csvfile = open('../data/uac/avalanche_geodata.csv','rU')
r = csv.reader(csvfile, dialect='excel')

header = r.next()

data = []
for row in r:
    data.append(row)

data = zip(*data)

dat = map(lambda s: datetime.strptime(s,"%m/%d/%y"), data[0])
lat = np.asarray(map(float,data[9]))
lon = np.asarray(map(float,data[10]))

start = datetime.strptime("11/01/12","%m/%d/%y")
days_since_start = np.asarray(map(lambda d: (d - start).days, dat))

'''
# Plot report dates
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("histogram of avalanche report dates")
pylab.hist(days_since_start,bins=181)
fig.show()
'''

uac_data_dict = {
    'date': dat,
    'latitude': lat,
    'longitude': lon
}

with open('../data/processed/UACdict2012-13.pkl','w') as f:
    pickle.dump(uac_data_dict,f)

pdb.set_trace()


