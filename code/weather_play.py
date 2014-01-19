import pygrib
import pdb
import numpy as np
import urllib

# Get data from the website, but only one at a time and only for the region we
# are interested in.
url_base = 'ftp://nomads.ncdc.noaa.gov/NAM/Grid218/'
w_path = '../data/weather/'
yyyy = '2012'
mm = '12'
dd = '01'
hhmm = '0000'
num = '000'
filename_base = 'nam_218_'
ext = '.grb'

#read the file
#u = urllib.urlopen(url_base+yyyy+mm+'/'+yyyy+mm+dd+'/'+filename_base+yyyy+mm+dd+'_'+hhmm+'_'+num+ext)
#f = open(w_path + filename_base+yyyy+mm+dd+'_'+hhmm+'_'+num + ext, 'wb')
#f.write(u.read())
#f.close()

# Hardcoded indexes for lat and lon for the wasatch range that we're interested
# in: lats[217:222,225:228]
#     array([[ 40.29480934,  40.30786135,  40.32080621],
#            [ 40.39959599,  40.41265419,  40.4256052 ],
#            [ 40.50432426,  40.51738863,  40.53034574],
#            [ 40.60899377,  40.62206426,  40.63502745],
#            [ 40.71360415,  40.72668073,  40.73964995]])
#     lons[217:222,225:228]
#     array([[-111.86382616, -111.72638645, -111.58891218],
#            [-111.88102612, -111.74344911, -111.60583742],
#            [-111.89826102, -111.76054643, -111.62279707],
#            [-111.91553097, -111.77767853, -111.63979122],
#            [-111.93283607, -111.79484551, -111.65681997]])
lat_minmax = 40.3,40.8
lon_minmax = -111.9,-111.6
lat_ind = 217,222
lon_ind = 225,228

grbs = pygrib.open(w_path + filename_base+yyyy+mm+dd+'_'+hhmm+'_'+num + ext)

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

# filter down to the wasatch range
lats = lats[lat_ind[0]:lat_ind[1],lon_ind[0]:lon_ind[1]]
lons = lons[lat_ind[0]:lat_ind[1],lon_ind[0]:lon_ind[1]]

# filter all data
dataset = []
for grb in filtered_grbs:
    dataset.append(grb.values[lat_ind[0]:lat_ind[1],lon_ind[0]:lon_ind[1]])

dataset = np.array(dataset)
pdb.set_trace()

grbs.close()
