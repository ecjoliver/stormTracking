'''

  Software for the tracking of storms and high-pressure systems

'''

#
# Load required modules
#

import numpy as np
from netCDF4 import Dataset

from matplotlib import pyplot as plt

import storm_functions as storm

#
# Load in slp data and lat/lon coordinates
#

# Parameters
pathroot = '/home/oliver/data/NCEP/20CRv2c/prmsl/6hourly/'

# Generate date and hour vectors
yearStart = 1851
yearEnd = 2014
t, dates, T, year, month, day, doy = storm.timevector([yearStart,1,1], [yearEnd,12,31]) # Daily
year = np.repeat(year, 4) # 6-hourly
month = np.repeat(month, 4) # 6-hourly
day = np.repeat(day, 4) # 6-hourly
hour = np.tile(np.array([0, 6, 12, 18]), T) # 6-hourly

# Load lat, lon
filename = pathroot + 'prmsl.' + str(yearStart) + '.nc'
fileobj = Dataset(filename, 'r')
lon = fileobj.variables['lon'][:].astype(float)
lat = fileobj.variables['lat'][:].astype(float)
fileobj.close()

# Load slp data
slp = np.zeros((0, len(lat), len(lon)))
for yr in range(yearStart, yearEnd+1):
    fileobj = Dataset(filename, 'r')
    filename = pathroot + 'prmsl.' + str(yr) + '.nc'
    slp0 = fileobj.variables['prmsl'][:].astype(float)
    slp = np.append(slp, slp0, axis=0)
    fileobj.close()
    print yr, slp0.shape[0]

#
# Storm Detection
#

# Initialisation

lon_storms_a = []
lat_storms_a = []
amp_storms_a = []
lon_storms_c = []
lat_storms_c = []
amp_storms_c = []

# Loop over time

T = slp.shape[0]

for tt in range(T):
    #
    print tt, T
    #
    # Detect lon and lat coordinates of storms
    #
    lon_storms, lat_storms, amp = storm.detect_storms(slp[tt,:,:], lon, lat, res=2, Npix_min=9, cyc='anticyclonic', globe=True)
    lon_storms_a.append(lon_storms)
    lat_storms_a.append(lat_storms)
    amp_storms_a.append(amp)
    #
    lon_storms, lat_storms, amp = storm.detect_storms(slp[tt,:,:], lon, lat, res=2, Npix_min=9, cyc='cyclonic', globe=True)
    lon_storms_c.append(lon_storms)
    lat_storms_c.append(lat_storms)
    amp_storms_c.append(amp)
    #
    # Save as we go
    #
    if (np.mod(tt, 100) == 0) + (tt == T-1):
        print 'Save data...'
    #
    # Combine storm information from all days into a list, and save
    #
        storms = storm.storms_list(lon_storms_a, lat_storms_a, amp_storms_a, lon_storms_c, lat_storms_c, amp_storms_c)
        np.savez('storm_det_slp', storms=storms, year=year, month=month, day=day, hour=hour)

