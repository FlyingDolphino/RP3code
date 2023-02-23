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
    
            
    N_gm_x = 10 #resolution of microphones eg 10 per length in x
    N_gm_y = 10
    
    #defines the max and min positions of the microphone grid
    max_x = 5 *Units.nmi
    min_x = -5 *Units.nmi
    max_y = 5 *Units.nmi
    min_y = 5 *Units.nmi
    
    
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

noise_calc(nexus)