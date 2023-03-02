# -*- coding: utf-8 -*-
"""
Created on Mon Jan 30 12:40:59 2023

@author: Alec
"""

import SUAVE
from SUAVE.Core import Units, Data 
import numpy as np
from SUAVE.Analyses.Process import Process
from SUAVE.Optimization.Nexus import Nexus
import Vehicles
import Analyses
import Missions
import Procedure
import pickle

def setup():

    procedure = Process()
    procedure.mission = noise_calc
    
    procedure.post_process = post_process
    
    
    return


def noise_calc(nexus):
    
            
    N_gm_x = 5 #number of microphones 
    N_gm_y = 5
    
    #defines the max and min positions of the microphone grid
    max_x = 4 *Units.nmi
    min_x = -2 *Units.nmi
    max_y = 2 *Units.nmi
    min_y = -4*Units.nmi

    
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
    
    y_limit = np.linspace(min_y,max_y,4)
    x_limit = np.linspace(min_x,max_x,4)
    
    spacingx = (x_limit[1]-x_limit[0])/(N_gm_x-1)
    spacingy = (y_limit[1]-y_limit[0])/(N_gm_y-1)
    
    Q_no = 1
    
    for i in range(len(x_limit)-1):
        for j in range(len(y_limit)-1):
            print('Processing Segment: '+str(Q_no))
               
            min_x = x_limit[i]
            max_x = x_limit[i+1]
            min_y = y_limit[j]
            max_y = y_limit[j+1]
            
            if Q_no ==1:
                max_y -= spacingy
                min_y -= spacingy
                max_x -= spacingx
                min_x -= spacingx
            elif Q_no ==2:
                max_x -= spacingx
                min_x -= spacingx
            elif Q_no==3:
                max_x -= spacingx
                min_x -= spacingx
                max_y += spacingy
                min_y += spacingy
            elif Q_no == 4:
                max_y -= spacingy
                min_y -= spacingy
            elif Q_no == 6:
                max_y += spacingy
                min_y += spacingy
            elif Q_no == 7:
                max_x += spacingx
                min_x += spacingx
                max_y -= spacingy
                min_y -= spacingy
            elif Q_no == 8:
                max_x += spacingx
                min_x += spacingx
            elif Q_no ==9:
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



def post_process(nexus):
    #find the weighted average sound here
    
    
    return nexus


def resultProcessing():
    ##load results here
    return
