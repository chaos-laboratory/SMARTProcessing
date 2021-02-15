import json
import numpy as np
import matplotlib
from matplotlib import cm
import matplotlib.pyplot as plt
import sys

path = sys.argv[1]
res = sys.argv[2]

#Do the right side hot pixels need to be erased?
fixH = True

with open(path) as file:
    data = json.load(file)

########### HELPER METHODS ##############
def fixHot():
    for frame in data['Melexis']:
        for i in range(63,768,32*2):
            frame[0][i] = avg(i,frame[0])


def avg(loc,arr):
    surr = []
    up = True
    down = True
    left = True
    right = True
    if loc < 32: up = False
    if loc > 735: down = False
    if loc % 32 == 0: left = False
    if loc % 32 == 31: right = False
    if up:
        surr.append(arr[loc-32])
        if left:
            surr.append(arr[loc-33])
        if right:
            surr.append(arr[loc-31])
    if down:
        surr.append(arr[loc+32])
        if left:
            surr.append(arr[loc+31])
        if right:
            surr.append(arr[loc+33])
    if left:
        surr.append(arr[loc-1])
    if right:
        surr.append(arr[loc+1])
    return np.mean(surr)

###########################################

#fix the hot pixels, if applicable
if fixH: fixHot()

arr = np.zeros((24,32,3,1))
copy = np.zeros((24,32,3,1))

final=[]

#generate the original array coordinates for sensor centered at (0,0)
for i in range(24):
    for j in range(32):
        #coordinates in spherical
        th = np.radians(-27.5+55/31*(j))
        ph = np.radians(72.5+35/23*(i))
        #coordinates in cartesian
        x = np.cos(th)*np.sin(ph);
        y = np.sin(th)*np.sin(ph);
        z = np.cos(ph);
        arr[i][j]=np.array([[x],[y],[z]])
        copy[i][j]=np.array([[x],[y],[z]])

for trial in data['Melexis']:
    theta = np.radians(trial[1][0])
    phi = np.radians(-(trial[1][1]-90))
    #generate rotational matrix
    R = np.array([[np.cos(theta)*np.cos(phi),-1*np.sin(theta),np.cos(theta)*np.sin(phi)],
                  [np.sin(theta)*np.cos(phi),np.cos(theta),np.sin(theta)*np.sin(phi)],
                  [-1*np.sin(phi),0,np.cos(phi)]])
    
    for i in range(24):
        for j in range(32):
            arr[i][j]=copy[i][j].copy()
    for i in range(24):
        for j in range(32):
            rot = R@arr[i][j]
            #use if you want output in cartesian
##            point = (rot[0][0],rot[1][0],rot[2][0],trial[0][32*i+j])
            
            #use if you want output in spherical
            th = np.degrees(np.arctan2(rot[1],rot[0]))[0]
            if th < 0:
                th = 360+th
            ph = np.degrees(np.arccos(rot[2]))[0]
            point = (th,ph,trial[0][32*i+j])
            final.append(point)

temps = [item[2] for item in final]
maxval = max(temps)
minval = min(temps)
std = np.std(temps)
mean = np.mean(temps)
#comment accordingly if you want to use straight min/max or stddev or custom values
#norm = matplotlib.colors.Normalize(vmin = minval, vmax = maxval)
norm = matplotlib.colors.Normalize(vmin = mean-std, vmax = mean+std)
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
