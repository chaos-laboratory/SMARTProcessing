import json
import numpy as np
import matplotlib
from matplotlib import cm
import sys
import turtle

#Do the right side hot pixels need to be erased?
fixH = True

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

def square(color,size):
    x = turtle.xcor()
    y = turtle.ycor()
    turtle.fillcolor(color)
    turtle.begin_fill()
    turtle.seth(0)
    turtle.fd(size)
    turtle.rt(90)
    turtle.fd(size)
    turtle.rt(90)
    turtle.fd(size)
    turtle.rt(90)
    turtle.fd(size)
    turtle.end_fill()
    turtle.rt(90)
    turtle.fd(size)

def drawFrame(data,size):
    for i in range(24):
        for j in range(32):
            rgb = colors.to_rgba(data[0][32*i+j])
            square((int(rgb[0]*256),int(rgb[1]*256),int(rgb[2]*256)),size)
        turtle.seth(180)
        turtle.fd(size*32)
        turtle.lt(90)
        turtle.fd(size)
    turtle.fd(10)

########### SETUP ##############
#load json data
file = sys.argv[1]
with open(file) as raw:
    data = json.load(raw)
#fix the hot pixels, if applicable
if fixH: fixHot()
#make colormap
temps = []
for frame in data["Melexis"]:
    temps+=frame[0]
maxval = max(temps)
minval = min(temps)
std = np.std(temps)
mean = np.mean(temps)
#comment norm accordingly if you want to use straight min/max or stddev
#norm = matplotlib.colors.Normalize(vmin = minval, vmax = maxval)
norm = matplotlib.colors.Normalize(vmin = mean-std, vmax = mean+std)
colors = cm.ScalarMappable(norm = norm, cmap = 'inferno')

#set up graphics
turtle.screensize(1000,1100)
turtle.speed(0)
turtle.colormode(255)
turtle.pu()
turtle.ht()
    
########### MAIN ##############
size = 5
count = 0

turtle.tracer(False)
#Draw write calls first for efficiency
turtle.goto(-450,500)
for i in range(7):
    turtle.seth(-90)
    turtle.fd(size*24+10)
    for j in range(5):
        turtle.write(data['Melexis'][i*5+j][1])
        turtle.seth(0)
        turtle.fd(size*32+10)
    turtle.seth(180)
    turtle.fd((size*32+10)*5)
    turtle.seth(-90)
    turtle.fd(10)

#draw frames
turtle.goto(-450,500)
for i in range(7):
    for j in range(5):
        drawFrame(data['Melexis'][i*5+j],size)
        turtle.seth(0)
        turtle.fd(size*32+10)
        turtle.lt(90)
        turtle.fd(size*24+10)
    turtle.seth(-90)
    turtle.fd(size*24+20)
    turtle.rt(90)
    turtle.fd((size*32+10)*5)
turtle.update()
turtle.done()
