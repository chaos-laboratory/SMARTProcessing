#Read a Grid-EYE scan from json and display all frames individually

import json
import numpy as np
import matplotlib
from matplotlib import cm
import sys
import turtle

########### SETUP ##############
#load json data
file = sys.argv[1]
with open(file) as raw:
    data = json.load(raw)
#Mirror the data? (use if taken with a flipped Grid-EYE)
mirror = True
#make colormap
temps = []
for frame in data["Thermal"]:
    temps+=frame[0]
maxval = max(temps)
minval = min(temps)
std = np.std(temps)
mean = np.mean(temps)
#comment norm accordingly if you want to use straight min/max or stddev or custom values
norm = matplotlib.colors.Normalize(vmin = minval, vmax = maxval)
#norm = matplotlib.colors.Normalize(vmin = mean-std, vmax = mean+std)
#norm = matplotlib.colors.Normalize(vmin = 19, vmax = 25)
colors = cm.ScalarMappable(norm = norm, cmap = 'inferno')

#set up graphics
turtle.screensize(500,500)
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
    for i in range(8):
        for j in range(8):
            if(mirror): rgb = colors.to_rgba(data[0][8*i+(7-j)])
            else: rgb = colors.to_rgba(data[0][8*i+j])
            square((int(rgb[0]*256),int(rgb[1]*256),int(rgb[2]*256)),size)
        turtle.seth(180)
        turtle.fd(size*8)
        turtle.lt(90)
        turtle.fd(size)
    turtle.fd(10)
    
########### MAIN ##############
size = 5
count = 0

turtle.tracer(False)
#Draw write calls first for efficiency
turtle.goto(-250,250)
for i in range(3):
    turtle.seth(-90)
    turtle.fd(size*8+10)
    for j in range(7):
        turtle.write(data['Thermal'][i*7+j][1])
        turtle.seth(0)
        turtle.fd(size*8+10)
    turtle.seth(180)
    turtle.fd((size*8+10)*7)
    turtle.seth(-90)
    turtle.fd(10)

#draw frames
turtle.goto(-250,250
            )
for i in range(3):
    for j in range(7):
        drawFrame(data['Thermal'][i*7+j],size)
        turtle.seth(0)
        turtle.fd(size*8+10)
        turtle.lt(90)
        turtle.fd(size*8+10)
    turtle.seth(-90)
    turtle.fd(size*8+20)
    turtle.rt(90)
    turtle.fd((size*8+10)*7)
turtle.update()
turtle.done()
