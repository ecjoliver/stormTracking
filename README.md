# stormTracking

Automated detection and tracking of atmospheric storms (cyclones) and high-pressure systems (anticyclones), given a series of mean sea level pressure maps. Developed as an adaptation of similar [mesoscale ocean eddy tracking code](https://github.com/ecjoliver/eddyTracking) and with modifications based on collaboration with Rebekah Cavanagh (Dalhousie University).

## Code Description

File                 |Description
---------------------|----------
|storm_detection.py    | Code for the detection of storms given a series of mean sea level pressure maps|
|storm_tracking.py     | Code for the tracking of storms after detection has been performed|
|storm_plot.py         | Code for plotting storm tracks (see figures)|
|storm_census.py       | Code for calculating census statistics of tracked storms (see figures)|
|storm_functions.py    | Module of supporting functions|
|figures/              | Folder containing figures of storm tracks and census plots based on 20CR data|

## Algorithm

Storms and anticylones are detected as extrema in the mean sea level pressure (slp) field. These extrema are detected following a modified form of the mesoscale ocean eddy tracking algorithm outlined in Chelton et al. (Progress in Oceanogaphy, 2011) and implemented in the [eddyTracking code](https://github.com/ecjoliver/eddyTracking).

The first step is to run the storm_detection.py script which will load in the slp fields, detect extrema (minima for cyclones, maxima for anticyclones). Extrema must lie within a set of pixels no fewer than Npix_min (recommended value: 9). The cyclone/anticyclone position is then recorded as the centre of mass of this neighbourhood of points. The detected positions are then stored in a .npz file.

The next step is to run the storm_tracking.py script which will load in the detected positions and stitch together appropriate tracks. The positions are linked from one time step to the next if they are the nearest neighbours within a search radius given by a maximum storm speed of 80 km/hour. Tracks are further filtered by removing short tracks with a duration 12 hours or less. The tracked storms and anticyclones are then stored in a .npz file.

## Notes

This code as been applied to 6-hourly mean sea level pressure maps from NCEP Twentieth Century Reanalysis (20CR). The code at the top of storm_detection.py will need to be modified for use with another data source, as will various other function options as necessary (e.g. time step, grid resolution, etc). The data files for the storm detection and storm tracks from 20CR, for use in the storm_plot.py and storm_census.py scripts, can be obtained here: [storm_det_slp.npz](http://passage.phys.ocean.dal.ca/~olivere/data/storm_det_slp.npz), [storm_track_slp.npz](http://passage.phys.ocean.dal.ca/~olivere/data/storm_track_slp.npz).

## Contact                                                                                                          
Eric C. J. Oliver  
Department of Oceanography  
Dalhousie University  
Halifax, Nova Scotia, Canada  
e: eric.oliver@dal.ca  
w: http://ecjoliver.weebly.com, https://github.com/ecjoliver
