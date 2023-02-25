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
import math

    
######MULTI QUADDRANT CODE

def resultProcessing():
    #Loads each quaddrant
    
    raw_data =[]
    for i in range (1,5):
        with open('resultsQ'+str((i)), 'rb') as f:
            temp = pickle.load(f)
            raw_data.append(temp)
     
            
    q1 = raw_data[0]
    q2 = raw_data[1]
    q3 = raw_data[2]
    q4 = raw_data[3]
    
    N_gm_x = q1.segments[0].analyses.noise.settings.level_ground_microphone_x_resolution 
    N_gm_y = q1.segments[0].analyses.noise.settings.level_ground_microphone_y_resolution
    
    #load flight path
    flightPath =[]
    for segment in q1.segments:
        flightPath.append(segment.conditions.frames.inertial.position_vector)        
    x_coords = np.array([arr[:,0] for arr in flightPath]).flatten()
    y_coords = np.array([arr[:,1] for arr in flightPath]).flatten()


    #grid assembly
    q1Grid = q1.segments[0].analyses.noise.settings.ground_microphone_locations
    q2Grid = q2.segments[0].analyses.noise.settings.ground_microphone_locations
    q3Grid = q3.segments[0].analyses.noise.settings.ground_microphone_locations
    q4Grid = q4.segments[0].analyses.noise.settings.ground_microphone_locations
    
    gridX = np.concatenate((q1Grid[:, 0], q2Grid[:, 0], q3Grid[:, 0], q4Grid[:, 0]))
    gridY = np.concatenate((q1Grid[:, 1], q2Grid[:, 1], q3Grid[:, 1], q4Grid[:, 1]))
    
    
    #SPL data formating
    q1SPL =[]
    q2SPL = []
    q3SPL =[]
    q4SPL = []
    
    for segment in q1.segments:
            for i in range(0,len(segment.conditions.noise.total_SPL_dBA)):
                q1SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                
    for segment in q2.segments:
            for i in range(0,len(segment.conditions.noise.total_SPL_dBA)):
                q2SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                
    for segment in q3.segments:
            for i in range(0,len(segment.conditions.noise.total_SPL_dBA)):
                q3SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                
    for segment in q4.segments:
            for i in range(0,len(segment.conditions.noise.total_SPL_dBA)):
                q4SPL.append(segment.conditions.noise.total_SPL_dBA[i])
    
    fullSPL = []
    for i in range(0,len(q1SPL)):
        fullSPL.append(np.concatenate((q1SPL[i],q2SPL[i],q3SPL[i],q4SPL[i])))
        
    
    X,Y, splData = gridSetup(N_gm_x, N_gm_y, gridX, gridY, fullSPL)
    
    
    #plotting function calls
    groundTrackplot(x_coords,y_coords,gridX,gridY)
    dBA_max_plot(X,Y,splData)







def groundTrackplot(x_coords,y_coords,gridX,gridY):
    
    fig, ax = plt.subplots()
    ax.scatter(x_coords, y_coords, color='blue')
    ax.scatter(gridX, gridY, color='red')
    
    # set the plot title and labels
    plt.title("Position Plot")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.axis('equal')

    # show the plot
    plt.show()

    return 














    
####SINGLE QUADDRANT CODE

#import results
with open('results.pkl','rb') as f:
    results = pickle.load(f)
    
def gridSetup(N_gm_x,N_gm_y,mx,my,zVals):
  
    sizeX =int( math.sqrt( N_gm_x**2 * 4))
    sizeY =int( math.sqrt(N_gm_y**2 * 4))
    
    mx = np.sort(mx)
    my = np.sort(my)
    
                
    for i in range(0,len(zVals)):
        zVals[i] = zVals[i].reshape(sizeX,sizeY)
    
    X = []
    for i in range(0,len(mx),N_gm_x*2):
        X.append(mx[i])
        
    Y = []
    for i in range(0,len(my),N_gm_x*2):
        Y.append(my[i])
      
    X = np.flip(X,axis=0)
    Y = np.flip(Y,axis=0)
    
    return X,Y,zVals

def timeStepPlot(X, Y, zVals, timestep):

    # Set up plot
    fig, ax = plt.subplots()

    # Set x and y axis limits
    ax.set_xlim([X.min(), X.max()])
    ax.set_ylim([Y.min(), Y.max()])
    
    # Set up color map
    cmap = plt.get_cmap('coolwarm')
    
    
    # Plot heatmap for current timestep
    im = ax.pcolormesh(X,Y,zVals[1], cmap=cmap, shading='auto')
        
     # Set title and color bar label
    ax.set_title(f'Timestep {timestep}')
    cbar = fig.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('dBA')
        
        # Show plot
    plt.show()
    return

def dBA_max_plot(X,Y,zVals):
    maxdBA = np.amax(zVals, axis=0)
    
    fig, ax = plt.subplots()

    # Set x and y axis limits
    ax.set_xlim([X.min(), X.max()])
    ax.set_ylim([Y.min(), Y.max()])
    
    # Set up color map
    cmap = plt.get_cmap('coolwarm')
    im = ax.pcolormesh(X,Y,maxdBA, cmap=cmap, shading='auto')
    ax.set_title('microphone maximum dBAs')
    cbar = fig.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('max dBA')
        
        # Show plot
    plt.show()
    return




resultProcessing()
