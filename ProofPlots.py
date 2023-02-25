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
    
def gridSetup(results):
        
    #setup microphone grid array
    N_gm_x = results.segments[0].analyses.noise.settings.level_ground_microphone_x_resolution 
    N_gm_y = results.segments[0].analyses.noise.settings.level_ground_microphone_y_resolution
        
    mData = results.segments[0].analyses.noise.settings.ground_microphone_locations
    mx = mData[:,0]
    my = mData[:,1]
    
    
    #array of the SPL of each microphone, for each control point
    zVals =[]
    for segment in results.segments:
            for i in range(0,len(segment.conditions.noise.total_SPL_dBA)):
                zVals.append(segment.conditions.noise.total_SPL_dBA[i])
                
    for i in range(0,len(zVals)):
        zVals[i] = zVals[i].reshape(N_gm_x,N_gm_y)
    
    X = []
    for i in range(0,len(mx),N_gm_x):
        X.append(mx[i])
        
    Y = []
    for i in range(0,N_gm_y):
        Y.append(my[i])
      
    X = np.flip(X,axis=0)
    Y = np.flip(Y,axis=0)
    
    return X,Y,zVals

def timeStepPlot(results, timestep):
    X, Y, zVals = gridSetup(results)
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

def dBA_max_plot(results):
    X, Y, zVals = gridSetup(results)
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