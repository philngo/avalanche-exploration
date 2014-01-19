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
'''
For reference
0 lat
1 lon
2 surface pressure
3 orography
4 surface temp
5 2 meter temp
6 dew_point_temp
7 wind_u_component
8 wind_v_component
9 total_precip
10 conv_precip
11 soil_temp
12 surface_rough
13 surface_sensible
14 surface_latent_flux
15 cloud_cover_grb
16 snow_fall_water_equivalents
17 snow_fall_water_equivalents
18 snow_depth_water_equivalents
19 soil_moisture
20 vegetation
21 ice_cover
22 albedo
23 surface_radiation
24 incident_solar
25 snowfall_gradient
'''

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

lat = data[:,0,:,:]
lon = data[:,1,:,:]
pressure = data[:,2,:,:]
orography = data[:,3,:,:] # not interesting
temp = data[:,4,:,:]
temp2m = data[:,5,:,:]
tempdewpoint = data[:,6,:,:]
wind_u = data[:,7,:,:]
wind_v = data[:,8,:,:]
precip_tot = data[:,9,:,:] # not sure how this is total precipitiation
precip_conv = data[:,10,:,:]
temp_soil = data[:,11,:,:]
surf_roughness = data[:,12,:,:] # not interesting
surf_flux_sens = data[:,13,:,:]
surf_flux_latent = data[:,14,:,:]
cloud_cover = data[:,15,:,:]
snowfall = data[:,16,:,:] # not sure of the diffs between these snow measures
snowfall2 = data[:,17,:,:]
snowdepth = data[:,18,:,:]
soilmoisture = data[:,19,:,:]
veg = data[:,20,:,:] # not interesting
ice = data[:,21,:,:] # not interesting
albedo = data[:,22,:,:]
surf_rad = data[:,23,:,:]
incedent_solar = data[:,24,:,:]
grad = data[:,25,:,:]

#make a dictionary
data_dict = {
    'latitude': lat,
    'longitude': lon,
    'pressure': pressure,
    'orography': orography,
    'temp': temp,
    'temp2m': temp2m,
    'tempdewpoint': tempdewpoint,
    'wind_u': wind_u,
    'wind_v': wind_v,
    'precip_tot': precip_tot,
    'precip_conv': precip_conv,
    'temp_soil': temp_soil,
    'surf_roughness': surf_roughness,
    'surf_flux_sens': surf_flux_sens,
    'surf_flux_latent': surf_flux_latent,
    'cloud_cover': cloud_cover,
    'snowfall': snowfall,
    'snowfall2': snowfall2,
    'snowdepth': snowdepth,
    'soilmoisture': soilmoisture,
    'veg': veg,
    'ice': ice,
    'albedo': albedo,
    'surf_rad': surf_rad,
    'incedent_solar': incedent_solar,
    'grad': grad,
}
# plot it!
with open('../data/processed/NAMdict2012-13.pkl','w') as f:
    pickle.dump(data_dict,f)

def plot_all(idx):
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_title(key[i])
    ax.plot(data[:,idx,:,0])
    ax.plot(data[:,idx,:,1])
    ax.plot(data[:,idx,:,2])
    fig.show()

idxs = range(2,3) + range(4,9) + range(10,12) + range(13,20) + range(22,26)

for i in idxs:
    plot_all(i)



pdb.set_trace()
