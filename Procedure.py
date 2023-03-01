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

def setup():

    procedure = Process()
    procedure.mission = noise_calc
    
    procedure.post_process = post_process
    
    
    return


def noise_calc(nexus):
    
            
    N_gm_x = 8 #resolution of microphones eg 10 per length in x
    N_gm_y = 8
    
    #defines the max and min positions of the microphone grid
    max_x = 7 *Units.nmi
    min_x = -3 *Units.nmi
    max_y = 3 *Units.nmi
    min_y = -5 *Units.nmi
    
    
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
    x_center = final_position_vector[3][0]
    y_center = final_position_vector[3][1]
    max_x +=x_center
    min_x += x_center
    max_y +=y_center
    min_y += y_center
    
    
    #sets up and runs the analysis with the noise simulation
    configs_analyses = Analyses.setup(configs,N_gm_x,N_gm_y,min_y,max_y,min_x,max_x,True)
    noise_mission = Missions.setup(configs_analyses,configs)
    configs.finalize()
    configs_analyses.finalize()
    noise_mission.finalize()
    
    print('evaluating noise mission with centered grid')
    nexus.results = noise_mission.evaluate()
    nexus.results = nexus.results.base
    
    print('done')
    
 
   
    return nexus



def post_process(nexus):
    #find the weighted average sound here
    
    
    return nexus


def resultProcessing():
    ##load results here
    return
