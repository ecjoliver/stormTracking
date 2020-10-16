'''

  Software for the tracking of storms and high-pressure systems

'''

#
# Load required modules
#

import numpy as np
from datetime import date
import cf_units as unit
from netCDF4 import Dataset

from matplotlib import pyplot as plt

import storm_functions as storm

import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--startyear', required=True, type=int)

args = parser.parse_args()
startyear=args.startyear
print('startyear = ', startyear)

#
# Load in slp data and lat/lon coordinates


dataset = 'NCEP_20CRV2C'
dataset = 'u-bl658'
#dataset = 'u-bb075'
#dataset = 'NCEP_R1'
#dataset = 'NCEP_CFSR'

# Parameters
pathroot = {'NCEP_20CRV2C': '/nesi/project/niwa00013/williamsjh/NZESM/storm/data/NCEP/20CRv2c/prmsl/6hourly/', 'NCEP_R1': '/home/oliver/data/NCEP/R1/slp/', 'NCEP_CFSR': '/home/oliver/data/NCEP/CFSR/prmsl/', 'u-bl658': '/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/u-bl658/','u-bb075': '/nesi/project/niwa00013/williamsjh/MASS/u-bb075/apc.pp/m01s16i222/'}
var = {'NCEP_20CRV2C': 'prmsl', 'NCEP_R1': 'slp', 'NCEP_CFSR': 'PRMSL_L101', 'u-bl658': 'air_pressure_at_sea_level', 'u-bb075': 'air_pressure_at_sea_level'}

# Generate date and hour vectors
yearStart = {'NCEP_20CRV2C': startyear, 'NCEP_R1': 1948, 'NCEP_CFSR': 1979, 'u-bl658': startyear, 'u-bb075': startyear}
yearEnd = {'NCEP_20CRV2C': startyear, 'NCEP_R1': 2017, 'NCEP_CFSR': 1979, 'u-bl658': startyear, 'u-bb075': startyear}

# Load lat, lon
filename = {'NCEP_20CRV2C': pathroot['NCEP_20CRV2C'] + 'prmsl.' + str(yearStart['NCEP_20CRV2C']) + '.nc',
            'NCEP_R1': pathroot['NCEP_R1'] + 'slp.' + str(yearStart['NCEP_R1']) + '.nc',
            'NCEP_CFSR': pathroot['NCEP_CFSR'] + 'prmsl.gdas.' + str(yearStart['NCEP_CFSR']) + '01.grb2.nc',
            'u-bl658': pathroot['u-bl658'] + 'regrid-bl658a.pc' + str(yearStart['u-bl658']) + '.nc', 
            'u-bb075': pathroot['u-bb075'] + 'regrid-bb075a.pc' + str(yearStart['u-bb075']) + '.nc' }
fileobj = Dataset(filename[dataset], 'r')
lon = fileobj.variables['lon'][:].astype(float)
lat = fileobj.variables['lat'][:].astype(float)
fileobj.close()

# Load slp data
slp = np.zeros((0, len(lat), len(lon)))
year = np.zeros((0,))
month = np.zeros((0,))
day = np.zeros((0,))
hour = np.zeros((0,))
for yr in range(yearStart[dataset], yearEnd[dataset]+1):
    if (dataset == 'NCEP_20CRV2C') + (dataset == 'NCEP_R1') :

        filename = {'NCEP_20CRV2C': pathroot['NCEP_20CRV2C'] + 'prmsl.' + str(yr) + '.nc', 'NCEP_R1': pathroot['NCEP_R1'] + 'slp.' + str(yr) + '.nc', 'u-bl658': pathroot['u-bl658'] + 'regrid-bl658a.pc' + str(yearStart['u-bl658']) + '.nc', 'u-bb075': pathroot['u-bb075'] + 'regrid-bb075a.pc' + str(yearStart['u-bb075']) + '.nc' }

        fileobj = Dataset(filename[dataset], 'r')
        time = fileobj.variables['time'][:]
        time_ordinalDays = time/24. + date(1800,1,1).toordinal()
        year = np.append(year, [date.fromordinal(np.floor(time_ordinalDays[tt]).astype(int)).year for tt in range(len(time))])
        month = np.append(month, [date.fromordinal(np.floor(time_ordinalDays[tt]).astype(int)).month for tt in range(len(time))])
        day = np.append(day, [date.fromordinal(np.floor(time_ordinalDays[tt]).astype(int)).day for tt in range(len(time))])
        hour = np.append(hour, (np.mod(time_ordinalDays, 1)*24).astype(int))
        slp0 = fileobj.variables[var[dataset]][:].astype(float)
        slp = np.append(slp, slp0, axis=0)
        fileobj.close()
        print(yr, slp0.shape[0])

    if (dataset == 'u-bl658') or (dataset == 'u-bb075') :

        filename = {'u-bl658': pathroot['u-bl658'] + 'regrid-bl658a.pc' + str(yearStart['u-bl658']) + '.nc', 'u-bb075': pathroot['u-bb075'] + 'regrid-bb075a.pc' + str(yearStart['u-bb075']) + '.nc' }

        fileobj = Dataset(filename[dataset], 'r')
        time = unit.num2date(fileobj.variables['time'][:], 'hours since 1970-01-01 00:00:00', unit.CALENDAR_360_DAY) 
        year = np.append(year, [time[tt].year for tt in range(len(time))])
        month = np.append(month, [time[tt].month for tt in range(len(time))])
        day = np.append(day, [time[tt].day for tt in range(len(time))])
        hour = np.append(hour, [time[tt].hour for tt in range(len(time))])
        print(year, month, hour, day)
        slp0 = fileobj.variables[var[dataset]][:].astype(float)
        slp = np.append(slp, slp0, axis=0)
        fileobj.close()
        print(yr, slp0.shape[0])

    if dataset == 'NCEP_CFSR':
        for mth in range(1, 12+1):
            filename = {'NCEP_CFSR': pathroot['NCEP_CFSR'] + 'prmsl.gdas.' + str(yr) + str(mth).zfill(2) + '.grb2.nc'}
            fileobj = Dataset(filename[dataset], 'r')
            time = fileobj.variables['time'][:]
            time_ordinalDays = time/24. + date(yr,mth,1).toordinal()
            year = np.append(year, [date.fromordinal(np.floor(time_ordinalDays[tt]).astype(int)).year for tt in range(len(time))])
            month = np.append(month, [date.fromordinal(np.floor(time_ordinalDays[tt]).astype(int)).month for tt in range(len(time))])
            day = np.append(day, [date.fromordinal(np.floor(time_ordinalDays[tt]).astype(int)).day for tt in range(len(time))])
            hour = np.append(hour, (np.mod(time_ordinalDays, 1)*24).astype(int))
            slp0 = fileobj.variables[var[dataset]][:].astype(float)
            slp = np.append(slp, slp0, axis=0)
            fileobj.close()
            print(yr, mth, slp0.shape[0])

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
    print(tt, T)
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
        print('Save data...')
    #
    # Combine storm information from all days into a list, and save
    #
        storms = storm.storms_list(lon_storms_a, lat_storms_a, amp_storms_a, lon_storms_c, lat_storms_c, amp_storms_c)
        np.savez('/nesi/project/niwa00013/williamsjh/NZESM/storm/model-data/u-bl658/u-bl658-storm_det_slp_'+str(startyear), storms=storms, year=year, month=month, day=day, hour=hour)

