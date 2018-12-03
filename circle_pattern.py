# -*- coding: utf-8 -*-
"""
Created on Mon Dec 25 11:57:53 2017

@author: User1
"""

import numpy as np
import matplotlib.pyplot as plt
import os
from sympy import *
from sympy.geometry import *
import turtle 

plt.style.use('ggplot')

d_nozzle = 0.35
# Set Initial X,Y,Z Possition
position = [40, 40, 0.3]
# Feed-rate / Speed
F = 1000
# Temperature of the Nozzle
Temp_C = 220
# Layer height
h_layer = 0.2
# Initial extrusion
E = 10
# Extrusion Area
A = (d_nozzle / 2) ** 2 * np.pi


#####################
#    Create file    #
#####################
# Get your current Directory
path = str(os.getcwd())
file = path + '\\tree.gcode'
f = open(file, "w+")
#####################
#    START CODE     #
#####################
f.writelines("M107 ;start with the fan off\n")
f.writelines("G21 ; set units to millimeters\n")
f.writelines("G90 ; use absolute coordinates\n")
f.writelines("M82 ; use absolute distances for extrusion\n")
f.writelines("G28 ; home all axes\n")
f.writelines("G1 Z10 F5000 ; lift nozzle \n")
f.writelines("M109 S%.3f ; set temperature \n" % (Temp_C))
f.writelines("G92 E0 ; zero the extruded length \n")
f.writelines("G1 X0 Y0 Z10 E%.3f ; extrude 10 mm of filament \n" % (E))
f.writelines("G1 X50 Y50 Z10 E%.3f ; extrude 10 mm of filament \n" % (E))       



def gcoder(X, Y, Z, F, A, f):
    E = 0
    f.writelines("G92 E0 \n")
    f.writelines("G10 \n")
    f.writelines("G0 X%.5f Y%.5f Z%.5f F%.3f \n" % (X[0], Y[0], Z, F))
    f.writelines("G11 \n")
    for i in range(0, len(X) - 1):        
        Distance = np.sqrt( abs((X[i + 1] - X[i]) ** 2 + (Y[i + 1] - Y[i]) ** 2))
        E = E + (Distance * A)
        f.writelines("G1 X%.5f Y%.5f Z%.5f E%.5f \n" % (X[i+1], Y[i+1], Z, E))
         

def outline(X, Y):
    Xmax = 0
    Ymax = 0
    Xmin = 200
    Ymin = 200    
    
    for i in X:
        if(i < Xmin):
            Xmin = i
        elif(i > Xmax):
            Xmax = i
    for i in Y:
        if(i < Ymin):
            Ymin = i
        elif(i > Ymax):
            Ymax = i
    plt.plot([Xmin,Xmin,Xmax,Xmax,Xmin], [Ymin,Ymax,Ymax,Ymin,Ymin])
    plt.show()
    plt.axis("equal")
    return Xmin, Ymin , Xmax, Ymax
      

def circle1234(X0, Y0, R, N):
    turtle.reset()
    turtle.speed(10)
    a = 200
    for i in range(a):
        turtle.penup()
        turtle.goto(X0, Y0)
        turtle.right(360/a)
        turtle.forward(R)
        turtle.forward(1)    
        turtle.penup()
        if(i%10 == 0):
            for i in range(a):
               turtle.right(360/a)
               turtle.forward(R)
               turtle.pendown()
               turtle.forward(1)    
               turtle.penup()
               turtle.left(180)
               turtle.forward(R+1)
               turtle.left(180)
    X, Y = turtle.
    return X, Y
circle1234(0,0,20,8) 


f.writelines("; Finish \n")
f.writelines("M104 S0 ;extruder heater off \n")
f.writelines("M140 S0 ;heated bed heater off (if you have it) \n")
f.writelines("G28 \n")
f.writelines("G90 ;absolute positioning \n")
f.writelines("G1 Y150 F5000 ;move completed part out\n")
f.writelines("M84 ;steppers off \n")
f.close()
