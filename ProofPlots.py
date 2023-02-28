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
    z_coords = np.array([arr[:,2] for arr in flightPath]).flatten()
    
    trajectory = np.stack((x_coords,y_coords,z_coords),axis=1)
    


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
                
                
    
    #this needs changing
    fullSPL = np.zeros((len(q1SPL),2*N_gm_x,2*N_gm_y))  
    for i in range(0,len(q1SPL)):
       
        fullSPL[i,0:N_gm_x,0:N_gm_y] =q1SPL[i].reshape(N_gm_x,N_gm_y)
        fullSPL[i,N_gm_x:,0:N_gm_y] = q2SPL[i].reshape(N_gm_x,N_gm_y)
        fullSPL[i,0:N_gm_x,N_gm_y:] = q3SPL[i].reshape(N_gm_x,N_gm_y)
        fullSPL[i,N_gm_x:,N_gm_y:]  = q4SPL[i].reshape(N_gm_x,N_gm_y)
            


    X,Y, splData = gridSetup(N_gm_x, N_gm_y, gridX, gridY, fullSPL)
    
    
    #plotting function calls
    groundTrackplot(trajectory,gridX,gridY)
    #dBA_max_plot(X,Y,splData)
    #timeStepPlot(X, Y, splData,5)
    cool3dPlot(X, Y, splData,trajectory)






def cool3dPlot(X,Y,Z,trajectory):
    # Define the functions to plot
        #from import of Z
    
    # Define the grid of points to plot
        #from import X and Y
    X,Y = np.meshgrid(X,Y)

    # Create the figure and 3D axes
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    levs   = np.linspace(33,70,33)
    
    # Create a slider widget
    axcolor = 'lightgoldenrodyellow'
    slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
    slider = Slider(slider_ax, 'Function', 0, 19, valinit=0, valstep=1)
    
    # Define the point to plot
    
    
    
    # Define the function to update the plot
    def update(val):
        ax.clear()
        ax.plot_surface(X, Y, Z[val], cmap='coolwarm')
        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        ax.set_zlabel('Z')
        ax.scatter(trajectory[val,0],trajectory[val,1],trajectory[val,2], color='black',levels = levs)
        ax.text(trajectory[val,0],trajectory[val,1],trajectory[val,2],  '%s' % (" 10,000"), size=20, zorder=1,  
        color='k') 
    
    # Attach the update function to the slider
    slider.on_changed(update)
    
    # Show the plot
    plt.show()
    



def groundTrackplot(trajectory,gridX,gridY):
    
    fig, ax = plt.subplots()
    ax.scatter(trajectory[:,0], trajectory[:,1], color='blue')
    ax.scatter(gridX, gridY, color='red')
    
    # set the plot title and labels
    plt.title("Position Plot")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.axis('equal')

    # show the plot
    plt.show()

    return 

    
def gridSetup(N_gm_x,N_gm_y,mx,my,zVals):
  
    sizeX =int( math.sqrt( N_gm_x**2 * 4))
    sizeY =int( math.sqrt(N_gm_y**2 * 4))
    
    mx = np.sort(mx)
    my = np.sort(my)
    
    
    X = []
    for i in range(0,len(mx),N_gm_x*2):
        X.append(mx[i])
        
    Y = []
    for i in range(0,len(my),N_gm_x*2):
        Y.append(my[i])
      

    

    
    return X,Y,zVals

def timeStepPlot(X, Y, zVals, timestep):

    # Set up plot
    fig, ax = plt.subplots()

    # Set x and y axis limits
    ax.set_xlim([np.min(X), np.max(X)])
    ax.set_ylim([np.min(Y), np.max(Y)])
    # Set up color map
    cmap = plt.get_cmap('coolwarm')
    
    
    levs   = np.linspace(33,70,33)
    im = ax.contourf(X , Y,zVals[timestep],levels = levs,  cmap=plt.cm.jet, extend='both') 
        
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
    ax.set_xlim([np.min(X), np.max(X)])
    ax.set_ylim([np.min(Y), np.max(Y)])
    
    # Set up color map
    levs   = np.linspace(33,70,33)
    im = ax.contourf(X , Y,maxdBA,levels = levs,  cmap=plt.cm.jet, extend='both') 
    ax.set_title('microphone maximum dBAs')
    cbar = fig.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('max dBA')
        
        # Show plot
    plt.show()
    return




resultProcessing()
