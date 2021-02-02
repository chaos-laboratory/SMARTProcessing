#Reads a single frame of thermal data of a specifed number of rows and columns
#(24x32 for Melexis, 8x8 for Grid-EYE) and draws it

import numpy as np
import matplotlib
from matplotlib import cm
import sys
import turtle

rows = int(sys.argv[1])
cols = int(sys.argv[2])

########### SETUP ##############
#Copy and paste the frame of temperatures here
temps = []
#make colormap
maxval = max(temps)
minval = min(temps)
std = np.std(temps)
mean = np.mean(temps)
#comment norm accordingly if you want to use straight min/max or stddev
#norm = matplotlib.colors.Normalize(vmin = minval, vmax = maxval)
norm = matplotlib.colors.Normalize(vmin = mean-std, vmax = mean+std)
colors = cm.ScalarMappable(norm = norm, cmap = 'inferno')

#set up graphics
turtle.screensize(320,240)
turtle.speed(0)
turtle.colormode(255)
turtle.pu()
turtle.ht()

########### HELPER METHODS ##############
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
    for i in range(rows):
        for j in range(cols):
            rgb = colors.to_rgba(temps[cols*i+j])
            square((int(rgb[0]*256),int(rgb[1]*256),int(rgb[2]*256)),size)
        turtle.seth(180)
        turtle.fd(size*cols)
        turtle.lt(90)
        turtle.fd(size)
    turtle.fd(10)
    
########### MAIN ##############
size = 10
count = 0

turtle.tracer(False)
turtle.goto(-160,120)
drawFrame(temps,size)
turtle.update()
turtle.done()
