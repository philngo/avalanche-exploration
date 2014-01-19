import csv
import datetime
import matplotlib.pyplot as plt
import numpy as np
import scipy
import pdb
import pickle
import pylab

# helper to make a range of datetime objects (one per day)
def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

key = ['lat','lon','surface_pressure','orography','surface temp','2 meter temp',\
       'dew point temp','wind u', 'wind v', 'total precip', 'convective precip',\
       'soil temp', 'surface roughness', 'surface sensible', 'surface latent flux',\
       'cloud cover', 'snow fall', 'snow fall 2', 'snow depth', 'soil moisture',\
       'vegetation','ice cover', 'albedo', 'surface radiation','incident solar',\
       'snowfall gradient']

start_d = datetime.date(2012,11,1)
end_d = datetime.date(2013,5,1)

full_winter_dataset = []
for d in daterange(start_d, end_d):
    filehandle = open('../data/weather/nam_218_'+str(d.year)+str(d.month).zfill(2)+str(d.day).zfill(2)+'.pkl','r')
    full_winter_dataset.append(pickle.load(filehandle))
    filehandle.close()

data = np.array(full_winter_dataset).reshape(181*8,26,5,3)

def plot_all(idx):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(key[i])
    ax.plot(data[:,idx,2,1])
    fig.show()

for i in range(2,3) + range(4,9) + range(10,12)+range(13,16)+range(17,20)+range(22,26):
    plot_all(i)

csvfile = open('../data/uac/avalanche_geodata.csv','rU')
r = csv.reader(csvfile, dialect='excel')

header = r.next()

data = []
for row in r:
    data.append(row)

data = zip(*data)

dates = map(lambda s: datetime.datetime.strptime(s,"%m/%d/%y"), data[0])
lat = np.asarray(map(float,data[9]))
lon = np.asarray(map(float,data[10]))

start = datetime.datetime.strptime("11/01/12","%m/%d/%y")
days_since_start = np.asarray(map(lambda d: (d - start).days, dates))

fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_title("histogram of avalanche report dates")
pylab.hist(days_since_start,bins=181)
fig.show()

pdb.set_trace()
