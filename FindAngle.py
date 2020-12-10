#reads in thermal json data, processes the 35 arrays, and outputs either .csv or .ply file

import json
import numpy as np
import matplotlib
from matplotlib import cm
import sys

#if res is ply or csv, change comments below accordingly
path = sys.argv[1]
res = sys.argv[2]

with open(path) as file:
    data = json.load(file)

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
            point = (rot[0][0],rot[1][0],rot[2][0],trial[0][32*i+j])
            
            #use if you want output in spherical
##            th = np.degrees(np.arctan2(rot[1],rot[0]))[0]
##            if th < 0:
##                th = 360+th
##            ph = np.degrees(np.arccos(rot[2]))[0]
##            point = (th,ph,trial[0][32*i+j])
            final.append(point)

therm = open(res,'w')

#write to ply file type
temps = [item[3] for item in final]
maxval = max(temps)
minval = min(temps)
std = np.std(temps)
mean = np.mean(temps)
#comment accordingly if you want to use straight min/max or stddev
#norm = matplotlib.colors.Normalize(vmin = minval, vmax = maxval)
norm = matplotlib.colors.Normalize(vmin = mean-std, vmax = mean+std)
colors = cm.ScalarMappable(norm = norm, cmap = 'inferno')

therm.write('''ply
format ascii 1.0
element vertex 26880
property float x
property float y
property float z
property uchar r
property uchar g
property uchar b
property float temp
end_header\n''')
for i in range(len(final)):
    cols = colors.to_rgba(final[i][3])
    therm.write(str(final[i][0])+' '+str(final[i][1])+' '+str(final[i][2])+' '+
                str(int(cols[0]*256))+' '+str(int(cols[1]*256))+' '+str(int(cols[2]*256))+' '+str(final[i][3])+'\n')
therm.close()

#Write to csv file type
##for i in range(3):
##    for j in range(len(final)):
##        therm.write(str(final[j][i])+',')
##    therm.write('\n')
##therm.close()



##temp_file = open(temp_path, 'r')
##lines = temp_file.readlines()
##new_temps = []
##for line in lines:
##    line = line.replace('\n', '')
##    line_ls = line.split(',')
##    line_ls = list(map(float, line_ls))
##    new_temps.append(line_ls)
##ls = list(zip(*new_temps))
##
##for i in range(len(final)):
##    equal=True
##    if final[i][0]!=ls[i][0]:
##        equal = False
##    if final[i][1]!=ls[i][1]:
##        equal = False
##    if final[i][2]!=ls[i][2]:
##        equal = False
####    if final[i][0]>ls[i][0]*1.0000001 or final[i][0]<ls[i][0]*0.9999999:
####        equal = False
####    if final[i][1]>ls[i][1]*1.0000001 or final[i][1]<ls[i][1]*0.9999999:
####        equal = False
####    if final[i][2]>ls[i][2]*1.0000001 or final[i][2]<ls[i][2]*0.9999999:
####        equal = False
##    if not equal:
##        print(i,final[i],ls[i])
        
    
