# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 11:29:06 2023

@author: Alec
"""

from SUAVE.Core import Units, Data
import numpy as np
import Vehicles
import Analyses
import Missions
import Procedure
import pickle
#import Plot_Mission
import SUAVE.Optimization.Package_Setups.scipy_setup as scipy_setup
import SUAVE.Optimization.Package_Setups.pyopt_setup as pyopt_setup
from SUAVE.Optimization.Nexus import Nexus
import pylab as plt

nexus = Nexus()
problem = Data()
nexus.optimization_problem = problem

nexus.vehicle_configurations = Vehicles.setup()
    
    # -------------------------------------------------------------------
    #  Analyses
    # -------------------------------------------------------------------
    
N_gm_x           = 10
N_gm_y           = 5
    
min_y = 1E-3 
max_y = 0.25*Units.nmi
min_x = -0.25*Units.nmi
max_x = 0.25*Units.nmi
    
    
nexus.analyses = Analyses.setup(nexus.vehicle_configurations,N_gm_x,N_gm_y,min_y,max_y,min_x,max_x,False)
    
    # -------------------------------------------------------------------
    #  Missions
    # -------------------------------------------------------------------
nexus.missions = Missions.setup(nexus.analyses,nexus.vehicle_configurations)
    
    # -------------------------------------------------------------------
    #  Procedure
    # -------------------------------------------------------------------    
nexus.procedure = Procedure.setup()


def noise_calc(nexus):
    
            
    N_gm_x = 5 #number of microphones 
    N_gm_y = 5
    
    #defines the max and min positions of the microphone grid
    max_x = 3 *Units.nmi
    min_x = -3 *Units.nmi
    max_y = 3 *Units.nmi
    min_y = -3 *Units.nmi
    
    spacingx = (max_x-min_x)/(N_gm_x+1)
    spacingy = (max_y-min_y)/(N_gm_y+1)
    
    
    #sets up the analysis
    configs = nexus.vehicle_configurations
    configs_analyses = Analyses.setup(configs,N_gm_x,N_gm_y,min_y,max_y,min_x,max_x,False) #Running the analysis without the noise simulation
    mission = Missions.setup(configs_analyses,configs)
    configs.finalize()
    configs_analyses.finalize()
    mission.finalize()
    print('Evaluating position mission')
    positionResults = mission.evaluate()
    print('Done')
    final_position_vector = positionResults.base.segments[-1].conditions.frames.inertial.position_vector
    



    
    #centralises the microphone grid on the end position of the aircraft
    x_center = final_position_vector[-1][0]
    y_center = final_position_vector[-1][1]
    max_x += x_center
    min_x += x_center
    max_y +=y_center
    min_y += y_center
    
    y_limit = np.linspace(min_y,max_y,3)
    x_limit = np.linspace(min_x,max_x,3)
    Q_no = 1
    
    for i in range(len(x_limit)-1):
        for j in range(len(y_limit)-1):
            print('Processing Quadrant: '+str(Q_no))
               
            min_x = x_limit[i]
            max_x = x_limit[i+1]
            min_y = y_limit[j]
            max_y = y_limit[j+1]
         
            if Q_no ==2:
                max_y += spacingy
                min_y += spacingy
            elif Q_no==3:
                max_x += spacingx
                min_x += spacingx
            elif Q_no == 4:
                max_y += spacingy
                min_y += spacingy
                max_x += spacingx
                min_x += spacingx

            
            #sets up and runs the analysis with the noise simulation
            configs_analyses = Analyses.setup(configs,N_gm_x,N_gm_y,min_y,max_y,min_x,max_x,True) 
            noise_mission = Missions.setup(configs_analyses,configs)
            configs.finalize()
            configs_analyses.finalize()
            noise_mission.finalize()
            
            nexus.results = noise_mission.evaluate()
            nexus.results = nexus.results.base
            print('done')
            
            
            filename = 'resultsQ'+str(Q_no)    
            with open(filename,'wb') as f:
                pickle.dump(nexus.results,f)
            Q_no +=1
    return nexus

def groundTrackplot(nexus):
    data = nexus.results
    
    mData = data.segments[0].analyses.noise.settings.ground_microphone_locations
    mx = mData[:,0]
    my = mData[:,1]
    
    positionData =[]
    for segment in data.segments:
        positionData.append(segment.conditions.frames.inertial.position_vector)
        
    x_coords = np.array([arr[:,0] for arr in positionData]).flatten()
    y_coords = np.array([arr[:,1] for arr in positionData]).flatten()

    
    fig, ax = plt.subplots()
    ax.scatter(x_coords, y_coords, color='blue')
    ax.scatter(mx, my, color='red')
    
    

    # set the plot title and labels
    plt.title("Position Plot")
    plt.xlabel("X Coordinate")
    plt.ylabel("Y Coordinate")
    plt.axis('equal')

    # show the plot
    plt.show()


noise_calc(nexus)
