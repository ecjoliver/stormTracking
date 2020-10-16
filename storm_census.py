'''

  Calculate storm census statistics
  for tracked storms

'''

#
# Load required modules
#

import numpy as np
import cartopy.crs as ccrs

import cf_units
import cartopy.feature as cfeature
from matplotlib import pyplot as plt
import mpl_toolkits.basemap as bm

#
# Load storm data
#

data = np.load('/nesi/project/niwa00013/williamsjh/NZESM/storm/data/NCEP/20CRv2c/prmsl/6hourly/storm_track_slp.npz', allow_pickle = True)
storms = data['storms']

#
# Some variables
#

# Cyclone properties
dt = 6. # Time step [hours]
age_min_hours = 72 # Minimum cyclone age to consider [hours]
age_min = age_min_hours/dt # [time steps]

# Census grid
lon = np.arange(0, 360+1, 2)
lat = np.arange(-90, 90+1, 2)
llon, llat = np.meshgrid(lon, lat)
X = len(lon)
Y = len(lat)
DIM = (Y,X)

#
# Calculate statistics
#

N = np.zeros(DIM) # Count of track positions
Nc = np.zeros(DIM) # Cyclones only
Na = np.zeros(DIM) # Anticyclones only
gen = np.zeros(DIM) # Count of genesis positions
genc = np.zeros(DIM)
gena = np.zeros(DIM)
term = np.zeros(DIM) # Count of termination positions
termc = np.zeros(DIM)
terma = np.zeros(DIM)
Nc_unique = np.zeros(DIM) # Unique counts
Na_unique = np.zeros(DIM)
counted = -1*np.ones(DIM, dtype=np.object)
amp = np.zeros(DIM) # Amplitude (central pressure)
ampc = np.zeros(DIM)
ampa = np.zeros(DIM)

for ed in range(len(storms)):
    print(ed, len(storms))
    if (storms[ed]['age'] >= age_min ):
        for t in range(storms[ed]['age']):
            i = np.where((lon > storms[ed]['lon'][t]-1) * (lon < storms[ed]['lon'][t]))[0]
            j = np.where((lat > storms[ed]['lat'][t]-1) * (lat < storms[ed]['lat'][t]))[0]
            if len(j)>0 and len(i)>0:
                # Count of storms and their average amplitude
                amp[j,i] += storms[ed]['amp'][t]
                N[j,i] += 1
                if storms[ed]['type'] == 'anticyclonic':
                    Na[j,i] += 1
                    ampa[j,i] += storms[ed]['amp'][t]
                else:
                    Nc[j,i] += 1
                    ampc[j,i] += storms[ed]['amp'][t]
                # Genesis (first location)
                if t == 0:
                    gen[j,i] += 1
                    if storms[ed]['type'] == 'anticyclonic':
                        gena[j,i] += 1
                    else:
                        genc[j,i] += 1
                # Termination (last location)
                if t == storms[ed]['age']-1:
                    term[j,i] += 1
                    if storms[ed]['type'] == 'anticyclonic':
                        terma[j,i] += 1
                    else:
                        termc[j,i] += 1
                # Unique counts
                firstcount = type(counted[j[0],i[0]])==type(-1)
                notcountedyet = False
                if not firstcount:
                    notcountedyet = not (ed in counted[j[0],i[0]])
                if firstcount or notcountedyet:
                    if storms[ed]['type'] == 'anticyclonic':
                        Na_unique[j,i] += 1
                    else:
                        Nc_unique[j,i] += 1
                    counted[j[0],i[0]] = np.append(counted[j[0],i[0]], ed)

# Calculate totals and averages as appropriate
N_unique = Nc_unique + Na_unique
cyc = Nc_unique / Na_unique
pcyc = Nc_unique / N_unique
amp /= N
ampc /= Nc
ampa /= Na

#
# Plots
#

# Set up projection
proj = bm.Basemap(projection='robin', lon_0=180, resolution='c')
lonproj, latproj = proj(llon, llat)

# Distribution of cyclone tracks and intensity (and for anticyclones)
# map projection i want to use
crs = ccrs.Robinson()

plt.figure(figsize=[15,15])

ax1 = plt.subplot(2,2,1,projection=ccrs.Robinson(central_longitude=180))
ax1.coastlines(linewidth = 0.5)
ax1.add_feature(cfeature.RIVERS)
plt.contourf(llon, llat, Nc_unique, levels=np.append(np.arange(0, 250+1, 25), 10000), cmap=plt.cm.hot_r,
           transform = ccrs.PlateCarree())#the transform kwarg here is the coord system of the original data
plt.title('Count of cyclone tracks')
H = plt.colorbar()
H.set_label('count')
plt.clim(0, 250)

ax2 = plt.subplot(2,2,2,projection=ccrs.Robinson(central_longitude=180))
ax2.coastlines(linewidth = 0.5)
ax2.add_feature(cfeature.RIVERS)
plt.contourf(llon, llat, ampc, 24, cmap=plt.cm.rainbow, transform = ccrs.PlateCarree())
H = plt.colorbar()
H.set_label('Pa')
plt.clim(95000, 101000)
plt.title('Average cyclone central pressure')

ax3 = plt.subplot(2,2,3,projection=ccrs.Robinson(central_longitude=180))
ax3.coastlines(linewidth=0.5)
ax3.add_feature(cfeature.RIVERS)
plt.contourf(llon, llat, Na_unique, levels=np.append(np.arange(0, 250+1, 25), 10000), cmap=plt.cm.hot_r,
             transform = ccrs.PlateCarree())
plt.title('Count of anticyclone tracks')
H = plt.colorbar()
H.set_label('count')
plt.clim(0, 250)

ax4 = plt.subplot(2,2,4,projection=ccrs.Robinson(central_longitude=180))
ax4.coastlines()
ax4.add_feature(cfeature.RIVERS)
plt.contourf(llon, llat, ampa, 24, cmap=plt.cm.rainbow,transform = ccrs.PlateCarree())
H = plt.colorbar()
H.set_label('Pa')
plt.clim(101000, 105000)
plt.title('Average anticyclone central pressure')
plt.savefig('figures/storm_distribution.png', bbox_inches='tight', pad_inches=0.05, dpi=300)

#  Distribution of cyclone genesis and termination points (and for anticyclones)
# map projection i want to use
crs = ccrs.Robinson()

plt.figure(figsize=[15,15])

ax1 = plt.subplot(2,2,1,projection=ccrs.Robinson(central_longitude=180))
ax1.coastlines(linewidth=0.5)
ax1.add_feature(cfeature.RIVERS)
plt.contourf(llon, llat, genc, levels=np.append(np.arange(0, 40+1, 5), 500), cmap=plt.cm.hot_r,
            transform = ccrs.PlateCarree())
plt.title('Count of cyclone genesis')
H = plt.colorbar()
H.set_label('count')
plt.clim(0, 40)

ax2 = plt.subplot(2,2,2,projection=ccrs.Robinson(central_longitude=180))
ax2.coastlines(linewidth=0.5)
ax2.add_feature(cfeature.RIVERS)
plt.contourf(llon, llat, termc, levels=np.append(np.arange(0, 40+1, 5), 500), cmap=plt.cm.hot_r,
            transform = ccrs.PlateCarree())
plt.title('Count of cyclone termination')
H = plt.colorbar()
H.set_label('count')
plt.clim(0, 40)

ax3 = plt.subplot(2,2,3,projection=ccrs.Robinson(central_longitude=180))
ax3.coastlines(linewidth=0.5)
ax3.add_feature(cfeature.RIVERS)
plt.contourf(llon, llat, gena, levels=np.append(np.arange(0, 40+1, 5), 500), cmap=plt.cm.hot_r,
            transform = ccrs.PlateCarree())
plt.title('Count of anticyclone genesis')
H = plt.colorbar()
H.set_label('count')
plt.clim(0, 40)

ax3 = plt.subplot(2,2,4,projection=ccrs.Robinson(central_longitude=180))
ax3.coastlines(linewidth=0.5)
ax3.add_feature(cfeature.RIVERS)
plt.contourf(llon, llat, terma, levels=np.append(np.arange(0, 40+1, 5), 500), cmap=plt.cm.hot_r,
            transform = ccrs.PlateCarree())
plt.title('Count of anticyclone termination')
H = plt.colorbar()
H.set_label('count')
plt.clim(0, 40)
plt.savefig('figures/storm_genesis_termination.png', bbox_inches='tight', pad_inches=0.05, dpi=300)

# Proportion of cyclones to anticyclones
# map projection i want to use
crs = ccrs.Robinson()

plt.figure(figsize=[15,15])

ax1 = plt.subplot(2,2,1,projection=ccrs.Robinson(central_longitude=180))
ax1.coastlines(linewidth=0.5)
ax1.add_feature(cfeature.RIVERS)

ax1.coastlines(linewidth=0.5)
plt.contourf(llon, llat, pcyc, 24, cmap=plt.cm.RdBu, transform = ccrs.PlateCarree())
plt.title('Proportion of cyclones (vs. anticyclones)')
H = plt.colorbar()
H.set_label('Proportion (1 = all cylones, 0 = all anticyclones)')
plt.clim(0, 1)
plt.savefig('figures/storm_proportion', bbox_inches='tight', pad_inches=0.05, dpi=300)

