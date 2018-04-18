# stormTracking

Automated detection and tracking of storms and anticyclones, given a series of mean sea level pressure maps.

## Code Description

File                 |Description
---------------------|----------
|storm_detection.py    | Code for the detection of storms given a series of sea level maps|
|storm_tracking.py     | Code for the tracking of storms after detection has been performed|
|storm_census.py       | Code for calculating census statistics of tracked storms|
|storm_plot.py         | Code for plotting storm tracks|
|storm_functions.py    | Module of supporting functions|

## Algorithm

Storms and anticylones are detected as extrema in the mean sea level pressure (slp) field. These extrema are detected following a modified form of the mesoscale ocean eddy tracking algorithm outlined in Chelton et al. (Progress in Oceanogaphy, 2011).

The first step is to run the storm_detection.py script which will load in the slp fields, detect extrema (minima for cyclones, maxima for anticyclones). Extrema must lie within a set of pixels no fewer than Npix_min (recommended value: 9). The cyclone/anticyclone position is then recorded as the centre of mass of this neighbourhood of points. The detected positions are then stored in a .npz file.

The next step is to run the storm_tracking.py script which will load in the detected positions and stitch together appropriate tracks. The positions are linked from one time step to the next if they are the nearest neighbours within a search radius given by a maximum storm speed of 80 km/hour. Tracks are further filtered by removing (i) short tracks with a total track length less than 1000 km or a duration less than 72 hours and (ii) meandering tracks that have a ratio of direct start-to-end distance less than 0.6 tims the total track length (following Klotzbach et al., Monthly Weather Review, 2016). The tracked storms and anticyclones are then stored in a .npz file.

## Notes

This code as been applied to 6-hourly mean sea level pressure maps from NCEP Twentieth Century Reanalysis (20CR). The code at the top of storm_detection.py will need to be modified for use with another data source, as will various other function options as necessary (e.g. time step, grid resolution, etc).

## Contact                                                                                                          
Eric C. J. Oliver  
Department of Oceanography  
Dalhousie University  
Halifax, Nova Scotia, Canada  
e: eric.oliver@dal.ca  
w: http://ecjoliver.weebly.com, https://github.com/ecjoliver
