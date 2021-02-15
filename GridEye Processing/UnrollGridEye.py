#Read in a Grid-EYE scan from Json and create a plot of the unrolled scan

import json
import numpy as np
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
import sys

#assume rectangular pixel coordinates?
rect = False

#Mirror the data? (use if taken with a flipped Grid-EYE)
mirror = True

path = sys.argv[1]
res = sys.argv[2]

with open(path) as file:
    data = json.load(file)

arr = np.zeros((8,8,3,1))
copy = np.zeros((8,8,3,1))

final=[]

if rect:
#generate the original array coordinates for sensor centered at (0,0)
    for i in range(8):
        for j in range(8):
            #coordinates in spherical
            th = np.radians(-30+60/7*(j))
            ph = np.radians(60+60/7*(i))
            #coordinates in cartesian
            x = np.cos(th)*np.sin(ph);
            y = np.sin(th)*np.sin(ph);
            z = np.cos(ph);
            arr[i][j]=np.array([[x],[y],[z]])
            copy[i][j]=np.array([[x],[y],[z]])
else:
#Estimated manually inputted actual locations of pixels based on
#this: https://cdn-learn.adafruit.com/assets/assets/000/043/261/original/Grid-EYE_SPECIFICATIONS%28Reference%29.pdf?1498680225
    thetaPixels = [-32.5,-23,-13.5,-4.5,4.5,13.5,23,32.5,
                   -31,-22,-13,-4,4,13,22,31,
                   -29.5,-21,-12.5,-4,4,12.5,21,29.5,
                   -29.5,-20.5,-12,-4,4,12,20.5,29.5,
                   -29.5,-20.5,-12,-4,4,12,20.5,29.5,
                   -29.5,-21,-12.5,-4,4,12.5,21,29.5,
                   -31,-22,-13,-4,4,13,22,31,
                   -32.5,-23,-13.5,-4.5,4.5,13.5,23,32.5]
    phiPixels = [-32.5,-30.5,-29.5,-29,-29,-29.5,-30.5,-32.5,
                 -23,-21.5,-21,-20.5,-20.5,-21,-21.5,-23,
                 -13.5,-12.5,-12,-12,-12,-12,-12.5,-13.5,
                 -4.5,-4.5,-4.5,-4.5,-4.5,-4.5,-4.5,-4.5,
                 4.5,4.5,4.5,4.5,4.5,4.5,4.5,4.5,
                 13.5,12.5,12,12,12,12,12.5,13.5,
                 23,21.5,21,20.5,20.5,21,21.5,23,
                 32.5,30.5,29.5,29,29,29.5,30.5,32.5]
    for i in range(64):
        phiPixels[i] = phiPixels[i]+90
    for i in range(8):
        for j in range(8):
            pos = i*8+j
            th = np.radians(thetaPixels[pos])
            ph = np.radians(phiPixels[pos])
            x = np.cos(th)*np.sin(ph);
            y = np.sin(th)*np.sin(ph);
            z = np.cos(ph);
            arr[i][j]=np.array([[x],[y],[z]])
            copy[i][j]=np.array([[x],[y],[z]])

for trial in data['Thermal']:
    theta = np.radians(trial[1][0])
    phi = np.radians(trial[1][1]-90)
    #generate rotational matrix
    R = np.array([[np.cos(theta)*np.cos(phi),-1*np.sin(theta),np.cos(theta)*np.sin(phi)],
                  [np.sin(theta)*np.cos(phi),np.cos(theta),np.sin(theta)*np.sin(phi)],
                  [-1*np.sin(phi),0,np.cos(phi)]])
    
    for i in range(8):
        for j in range(8):
            arr[i][j]=copy[i][j].copy()
    for i in range(8):
        for j in range(8):
            rot = R@arr[i][j]
            #use if you want output in cartesian
##            point = (rot[0][0],rot[1][0],rot[2][0],trial[0][32*i+j])
            
            #use if you want output in spherical
            th = np.degrees(np.arctan2(rot[1],rot[0]))[0]
            if th < 0:
                th = 360+th
            ph = np.degrees(np.arccos(rot[2]))[0]
            if(mirror): temp = trial[0][8*i+(7-j)]
            else: temp = trial[0][8*i+j]
            point = (th,ph,temp)
            final.append(point)

temps = [item[2] for item in final]
maxval = max(temps)
minval = min(temps)
std = np.std(temps)
mean = np.mean(temps)
#comment accordingly if you want to use straight min/max or stddev or custom values
norm = matplotlib.colors.Normalize(vmin = minval, vmax = maxval)
#norm = matplotlib.colors.Normalize(vmin = mean-std, vmax = mean+std)
#norm = matplotlib.colors.Normalize(vmin = 19, vmax = 25)
colors = cm.ScalarMappable(norm = norm, cmap = 'inferno')

fig = plt.figure(figsize=(8,5), dpi=300)
ax = fig.add_subplot(111)
textsize=20
thetas = [i[0] for i in final]
phis = [i[1] for i in final]

ax.scatter(thetas,phis,c=colors.to_rgba(temps),marker='o',cmap='inferno')
axes = plt.gca()
plt.savefig(res,dpi=600, format='png')
