import pygrib
import pdb
import os
import pickle
import numpy as np
import urllib
import datetime

# Get data from the website, but only one at a time and only for the region we
# are interested in.
url_base = 'ftp://nomads.ncdc.noaa.gov/NAM/Grid218/'
w_path = '../data/weather/'

def dataset_from_datetime(d):
    # extract strings
    yyyy = str(d.year)
    mm = str(d.month).zfill(2)
    dd = str(d.day).zfill(2)
    # half of this is forecast, half is prediction 3 hours in future
    hhmm = ['0000_000','0000_003','0600_000','0600_003',\
            '1200_000','1200_003','1800_000','1800_003']
    filename_base = 'nam_218_'
    ext = '.grb'

    # latitude and longitude ranges covering the wasatch
    lat_minmax = 40.3,40.8
    lon_minmax = -111.9,-111.6
    lat_ind = 217,222
    lon_ind = 225,228

    full_day_dataset = []
    for t in hhmm:
        #read the file
        u = urllib.urlopen(url_base+yyyy+mm+'/'+yyyy+mm+dd+'/'+filename_base+yyyy+mm+dd+'_'+t+ext)
        f = open(w_path + filename_base+yyyy+mm+dd+'_'+t+ext, 'wb')
        f.write(u.read())
        f.close()

        grbs = pygrib.open(w_path + filename_base+yyyy+mm+dd+'_'+t + ext)

        surface_press_grb = grbs.select(name='Surface pressure', level=0) #3
        orography_grb = grbs.select(name='Orography') #4
        surface_temp_grb = grbs.select(name='Temperature', level=0) #5
        two_m_temp_grb = grbs.select(name='2 metre temperature', level=2) #6
        dew_point_temp_grb = grbs.select(name='Dew point temperature', level=2) #7
        wind_u_comp_grb = grbs.select(name='10 metre U wind component', level=10) #9
        wind_v_comp_grb = grbs.select(name='10 metre V wind component', level=10) #10
        total_precip_grb = grbs.select(name='Total Precipitation') #11
        conv_precip_grb = grbs.select(name='Convective precipitation (water)') #12
        soil_temp_grb = grbs.select(name='Soil Temperature') #291
        surface_rough_grb = grbs.select(name='Surface roughness', level=0) #299
        surface_sensible_flux_grb = grbs.select(name='Surface sensible heat flux', level=0) #301
        surface_latent_flux_grb = grbs.select(name='Surface latent heat flux', level=0) #302
        cloud_cover_grb = grbs.select(name='Total Cloud Cover', level=0) #358
        snow_fall_water_eq_grb = grbs.select(name='Snow Fall water equivalent') #361
        snow_depth_water_eq_grb = grbs.select(name='Snow depth water equivalent') #362
        soil_moisture_grb = grbs.select(name='Soil Moisture') #378
        vegetation_grb = grbs.select(name='Vegetation fraction') #381
        ice_cover_grb = grbs.select(name='Ice cover (1=land, 0=sea)') #382
        albedo_grb = grbs.select(name='Albedo') #383
        surface_rad_grb = grbs.select(name='Surface net thermal radiation, clear sky gradient', level=1) #384
        incident_solar_grb = grbs.select(name='TOA incident solar radiation gradient', level=0) #385
        snowfall_gradient_grb = grbs.select(name='Large scale snowfall gradient', level=0) #388


        filtered_grbs = [surface_press_grb[0],\
                         orography_grb[0],\
                         surface_temp_grb[0],\
                         two_m_temp_grb[0],\
                         dew_point_temp_grb[0],\
                         wind_u_comp_grb[0],\
                         wind_v_comp_grb[0],\
                         total_precip_grb[0],\
                         conv_precip_grb[0],\
                         soil_temp_grb[0],\
                         surface_rough_grb[0],\
                         surface_sensible_flux_grb[0],\
                         surface_latent_flux_grb[0],\
                         cloud_cover_grb[0],\
                         snow_fall_water_eq_grb[0],\
                         snow_fall_water_eq_grb[1],\
                         snow_depth_water_eq_grb[0],\
                         soil_moisture_grb[0],\
                         vegetation_grb[0],\
                         ice_cover_grb[0],\
                         albedo_grb[0],\
                         surface_rad_grb[0],\
                         incident_solar_grb[0],\
                         snowfall_gradient_grb[0]]

        lats, lons = filtered_grbs[0].latlons()


        # filter all data
        hour_dataset = []
        hour_dataset.append(lats[lat_ind[0]:lat_ind[1],lon_ind[0]:lon_ind[1]])
        hour_dataset.append(lons[lat_ind[0]:lat_ind[1],lon_ind[0]:lon_ind[1]])
        for grb in filtered_grbs:
            hour_dataset.append(grb.values[lat_ind[0]:lat_ind[1],lon_ind[0]:lon_ind[1]])

        full_day_dataset.append(np.array(hour_dataset))
        grbs.close()
        os.remove(w_path + filename_base+yyyy+mm+dd+'_'+t+ ext)

    filehandle = open(w_path + filename_base+yyyy+mm+dd+'.pkl','w')
    pickle.dump(full_day_dataset,filehandle)
    filehandle.close()
    return np.array(full_day_dataset)

start_d = datetime.date(2012,11,1)
end_d = datetime.date(2013,5,1)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + datetime.timedelta(n)

full_winter_dataset = []
for d in daterange(start_d, end_d):
    full_winter_dataset.append(dataset_from_datetime(d))

full_winter_dataset = np.array(full_winter_dataset)

#pickle it so we can use it later
filehandle = open('data_winter2012-13.pkl','w')
pickle.dump(full_winter_dataset,filehandle)
filehandle.close()
