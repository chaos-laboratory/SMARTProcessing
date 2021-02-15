# SMARTProcessing
Scripts for post-processing and displaying SMART data

## Code
Most scripts were intended for standalone use depending on the desired output

### *Melexis Processing*

### fix.py
*Overview* - Fixes incorrectly formatted JSON data coming from EEPFL SMaRT sensor running outdated code

*Input* - File containing incorrectly formatted JSON data for the 35 individual temperature arrays

*Output* - Rewrites file with corrected data

### viz_lidar.py
*Overview* - Matches each Lidar point with the nearest thermal point 

*Input* - File containing JSON data for Lidar points and 35 temperature arrays, output file

*Output* - .pts formatted file containing each point (in cartesian), associated temperature, and color

*Useage notes* - Comment around line 63 depending on the desired style of normalization for the colormap. Adjust flip variable (line 14) depending on how Melexis is mounted in comparison to LIDAR (flip if mounted in opposite directions)

### *GridEye Processing*

### ShowThermalGridEye.py 
*Overview* - Displays a layout of all 21 frames from a Grid-EYE scan 

*Input* - File containing JSON data for the 21 individual temperature arrays and their directions

*Output* - Displays all 21 frames and their directions

*Useage notes* - Comment around line 25 depending on the desired style of normalization for the colormap. Normalization is based on all temperatures from the entire scan, not each frame individually. Adjust mirrored variable (line 14) depending on orientation of Grid-EYE

### UnrollGridEye.py
*Overview* - Displays a Grid-EYE scan graphed on a plane by theta/phi

*Input* - File containing JSON data for the 21 individual temperature arrays and their directions, output filepath (.png reccomended)

*Output* - Unrolled scan image

*Useage notes* - Comment around line 104 depending on the desired style of normalization for the colormap. Adjust rect variable (line 11) depending on whether estimated rectangular pixel mapping is desired. Adjust mirrored variable (line 14) depending on orientation of Grid-EYE (note: script was written for an upside-down sensor and will not currently function with a correctly oriented one)

### *Files for Processing either GridEye or Melexis*

### FindAngle.py
*Overview* - Transforms raw Melexis data by reading 35 individual frames and mapping each pixel to a direction

*Input* - a file containing JSON data for the 35 individual temperature arrays and their directions

*Output* - a .csv or .ply file containing each pixel and its associated direction in either spherical or cartesian coordinates

*Useage notes* - Some commenting/uncommenting is necessary depending on desired output in 3 areas: Spherical vs cartesian output (line 48), temperature colormap norm (line 67), and output file type (line 61)

### Heat3d.pde
*Overview* - Displays thermal data from a .csv file 

*Input* - .csv file with each line formatted (theta, phi, temp)

*Output* - Rotatable spherical mapping of temperature points

*Useage notes* - Unlike the .py files, where input files are meant to be arguments in the command line, the input file must be manually typed into the file

### ShowArray.py
*Overview* - Displays a single frame of thermal data. Intended for either Melexis (24x32) or Grid-EYE (8x8) data

*Input* - Number of rows and columns of the frame

*Output* - A display of the frame, colored by temperature

*Usage notes* - Data must be manually copied into line 15. Comment around line 21 depending on the desired style of normalization for the colormap
