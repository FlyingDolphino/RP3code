# -*- coding: utf-8 -*-
"""
Created on Fri Feb 24 14:26:37 2023

@author: Alec
"""

from SUAVE.Core import Units, Data
import pickle
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
from matplotlib.widgets import Slider


#import results
with open('results.pkl','rb') as f:
    results = pickle.load(f)
    

#setup microphone grid array
mData = results.segments[0].conditions.noise.ground_microphone_locations[0]
mx = mData[:,0]
my = mData[:,1]


#array of the SPL of each microphone, for each control point
zVals =[]
for segment in results.segments:
        for i in range(0,len(segment.conditions.noise.total_SPL_dBA)):
            zVals.append(segment.conditions.noise.total_SPL_dBA[i])
        






# Define the grid of points to plot



# Create the figure and 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

# Create a slider widget
axcolor = 'lightgoldenrodyellow'
slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
slider = Slider(slider_ax, 'Time Step', 0, len(zVals)-1, valinit=0, valstep=1)

# Define the function to update the plot
def update(val):
    X,Y = np.meshgrid(mx,my)
    Z = zVals[slider.val]
    ax.clear()
    ax.plot_surface(mx, my, Z, cmap='coolwarm')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title('Time Step = {}'.format(int(slider.val)))
    for i in range(len(mx)):
        for j in range(len(my)):
            ax.scatter(mx[i], my[j], zVals[i,j], color='black')
            ax.text(mx[i], my[j], zVals[i,j], '%s' % (" {:.2f}".format(zVals[i,j])), 
                    size=8, zorder=1, color='k') 

# Attach the update function to the slider
slider.on_changed(update)

# Update the plot for the initial time step
update(0)

# Show the plot
plt.show()