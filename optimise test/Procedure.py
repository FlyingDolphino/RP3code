# -*- coding: utf-8 -*-
"""
Created on Tue Mar  7 14:00:11 2023

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
from SUAVE.Optimization.write_optimization_outputs import write_optimization_outputs
import pickle as pkl

def setup():

    procedure = Process()
    procedure.missions = Process()
    procedure.missions = noiseRun
    procedure.post_process = postProcess
    
    
    return procedure


def noiseRun(nexus):
    #get speed and approach rate from nexus

    
    N_gm_x = 4 #number of microphones 
    N_gm_y = 4
    
    #defines the max and min positions of the microphone grid
    max_x = 6 *Units.nmi
    min_x = -6 *Units.nmi
    max_y = 6 *Units.nmi
    min_y = -6*Units.nmi
    configs = nexus.vehicle_configurations
    configs_analyses = Analyses.setup(configs,N_gm_x,N_gm_y,min_y,max_y,min_x,max_x,False) #Running the analysis without the noise simulation
    ##configs_analyses.finalize()
    missiontest = Missions.setup(configs_analyses,nexus.vehicle_configurations)
    missiontest = updateMissionWithOptimiseValues(nexus,missiontest)  


    #somehow pass the new analyses into mission from nexus
    nexus.missions = missiontest
    nexus.analyses = configs_analyses
    nexus.analyses.finalize()


    mission = nexus.missions.base

   

    print('Evaluating position mission')
    positionResults = mission.evaluate()
    print('Done')
    final_position_vector = positionResults.segments[-1].conditions.frames.inertial.position_vector
    
    x_center = final_position_vector[-1][0]
    y_center = final_position_vector[-1][1]
    max_x += x_center
    min_x += x_center
    max_y +=y_center
    min_y += y_center
    
    
    print('run noise')
    configs_analyses = Analyses.setup(configs,N_gm_x,N_gm_y,min_y,max_y,min_x,max_x,True) 
    missiontest = Missions.setup(configs_analyses,nexus.vehicle_configurations)
    missiontest = updateMissionWithOptimiseValues(nexus,missiontest)  


    nexus.missions = missiontest
    nexus.analyses = configs_analyses
    noise_mission = nexus.missions.base
   ## configs.finalize()
    nexus.analyses.finalize()
    results = nexus.results
    results.base = noise_mission.evaluate()

    print('done')
    
    return nexus

def postProcess(nexus):
    
    nexus.total_number_of_iterations +=1
    res = nexus.results.base
    control_points = len(res.segments[0].conditions.noise.total_SPL_dBA)
    micro = res.segments[0].conditions.noise.number_ground_microphones
    
    
    SPL = []
    squaredSPL = []
    for segment in res.segments:
            for i in range(0,control_points):
                SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                squaredSPL.append(segment.conditions.noise.total_SPL_dBA[i]**2)
   
        
    rms_array = np.sqrt(np.nanmean(squaredSPL, axis=0))
    if np.isnan(rms_array).any():
        print("Array contains nan values")
    if np.isinf(rms_array).any():
        print("Array contains inf values")
    
    maxDba = np.nanmax(SPL,axis=0)
    maxLinear = maxDba
    for i in range(0,len(maxDba)):
        maxLinear[i] = 10**(maxDba[i]/10)
    
    
    avg = maxLinear.sum()/micro
    avg1 = rms_array.sum()/micro
    summary = nexus.summary
    max_throttle = 0
    min_throttle = 1
    for segment in res.segments.values():
        max_segment_throttle = np.max(segment.conditions.propulsion.throttle[:,0])
        min_segment_throttle = np.min(segment.conditions.propulsion.throttle[:,0])
        if max_segment_throttle > max_throttle:
            max_throttle = max_segment_throttle
        if min_throttle > min_segment_throttle:
            min_throttle = min_segment_throttle
            
            
    summary.max_throttle = max_throttle
    summary.min_throttle = min_throttle
    summary.avgdBA = avg1
    
    filename = 'results.txt'
    write_optimization_outputs(nexus, filename)
 

    return nexus 
def updateMissionWithOptimiseValues(nexus,mission):
    #get speed and approach rate from nexus


    speed = nexus.missions.base.segments.initial_approach.air_speed
    approach_rate = nexus.missions.base.segments.final_approach.descent_rate
    verticalHeight = nexus.missions.base.segments.vertical_landing.altitude_start
    turn_to_base = nexus.missions.base.segments.turn_to_final.true_course
    turn_to_final = nexus.missions.base.segments.final_approach.true_course
    
    
    
    
    mission.base.segments.initial_approach.air_speed = speed
    mission.base.segments.turn_to_final.air_speed=  speed
    mission.base.segments.final_approach.air_speed= speed
    mission.base.segments.descent_transition.air_speed_start= speed 
    mission.base.segments.final_approach.descent_rate = approach_rate
    mission.base.segments.vertical_landing.altitude_start = verticalHeight
    mission.base.segments.descent_transition.altitude = verticalHeight
    mission.base.segments.final_approach.altitude_end = verticalHeight
    mission.base.segments.turn_to_final.true_course = turn_to_base
    mission.base.segments.final_approach.true_course = turn_to_final
    mission.base.segments.descent_transition.true_course = turn_to_final
    mission.base.segments.vertical_landing.true_course = turn_to_final
    
    print('Optimiser input :speed: ',speed)
    print('Optimiser input :approach rate: ',approach_rate)
    print('Optimiser input :Hover Height ',verticalHeight)



    return mission
     

