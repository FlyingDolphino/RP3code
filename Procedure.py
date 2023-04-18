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
from SUAVE.Optimization.write_optimization_outputs import write_optimization_outputs
import pickle

def setup():

    procedure = Process()
    procedure.mission = noise_calc
    procedure.post_process = post_process
    
    
    return procedure


def noise_calc(nexus):
    
            
    N_gm_x = 4 #number of microphones 
    N_gm_y = 4
    
    #defines the max and min positions of the microphone grid
    max_x = 5 *Units.nmi
    min_x = -5 *Units.nmi
    max_y = 5 *Units.nmi
    min_y = -5*Units.nmi

    
    #sets up the analysis
    configs = nexus.vehicle_configurations
    configs_analyses = Analyses.setup(configs,N_gm_x,N_gm_y,min_y,max_y,min_x,max_x,False) #Running the analysis without the noise simulation
    missionUpdate = Missions.setup(configs_analyses,configs)
    missionUpdate = updateMissionWithOptimiseValues(nexus,missionUpdate)

    nexus.missions = missionUpdate
    nexus.analyses = configs_analyses
    nexus.analyses.finalize()
    mission = nexus.missions.base
    print('Evaluating position mission')
    positionResults = mission.evaluate()
    print('Done')
    final_position_vector = positionResults.segments[-1].conditions.frames.inertial.position_vector

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
            missionUpdate = Missions.setup(configs_analyses,nexus.vehicle_configurations)
            missionUpdate = updateMissionWithOptimiseValues(nexus,missionUpdate)  

            nexus.missions = missionUpdate
            nexus.analyses = configs_analyses
            noise_mission = nexus.missions.base
            nexus.analyses.finalize()
            nexus.results = noise_mission.evaluate()
            

            print('done')
            
            
            filename = 'resultsQ'+str(Q_no)    
            with open(filename,'wb') as f:
                pickle.dump(nexus.results,f)
            Q_no +=1
            
    return nexus


def post_process(nexus):
    nexus.total_number_of_iterations +=1
     
    SPLdata, micro = resultsProcessing()

    res = nexus.results
    
    rms_array = np.sqrt(np.nanmean(SPLdata, axis=0))

        
    avg = rms_array.sum()/micro
    
    
    
    
    
    
    
    
    summary = nexus.summary
    max_throttle = 0
    min_throttle = 1
    for segment in res.segments.values():
        max_segment_throttle = np.max(segment.conditions.propulsion.throttle[:,0])
        min_segment_throttle = np.min(segment.conditions.propulsion.throttle[:,0])
        if max_segment_throttle > max_throttle:
            max_throttle = max_segment_throttle
        elif min_throttle > min_segment_throttle:
            min_throttle = min_segment_throttle
            
            
    summary.max_throttle = max_throttle
    summary.min_throttle = min_throttle
    summary.avgdBA = avg
    filename = 'results.txt'
    write_optimization_outputs(nexus, filename)
    print(avg)
    
    return nexus


def resultsProcessing():
    #Loads each quaddrant
    
    raw_data =[]
    for i in range (1,10):
        with open('resultsQ'+str((i)), 'rb') as f:
            temp = pickle.load(f)
            raw_data.append(temp)
     
            
    q1 = raw_data[0]
    q2 = raw_data[1]
    q3 = raw_data[2]
    q4 = raw_data[3]
    q5 = raw_data[4]
    q6 = raw_data[5]
    q7 = raw_data[6]
    q8 = raw_data[7]
    q9 = raw_data[8]
    
    N_gm_x = q1.segments[0].analyses.noise.settings.level_ground_microphone_x_resolution 
    N_gm_y = q1.segments[0].analyses.noise.settings.level_ground_microphone_y_resolution
    control_points = len(q1.segments[0].conditions.noise.total_SPL_dBA)
    micro = q1.segments[0].conditions.noise.number_ground_microphones*9
    
    
    #SPL data formating
    q1SPL =[]
    q2SPL = []
    q3SPL =[]
    q4SPL = []
    q5SPL = []
    q6SPL =[]
    q7SPL=[]
    q8SPL=[]
    q9SPL=[]
    
    for segment in q1.segments:
            for i in range(0,control_points):
                q1SPL.append(segment.conditions.noise.total_SPL_dBA[i]**2)
                
    for segment in q2.segments:
            for i in range(0,control_points):
                q2SPL.append(segment.conditions.noise.total_SPL_dBA[i]**2)
                
    for segment in q3.segments:
            for i in range(0,control_points):
                q3SPL.append(segment.conditions.noise.total_SPL_dBA[i]**2)
                
    for segment in q4.segments:
            for i in range(0,control_points):
                q4SPL.append(segment.conditions.noise.total_SPL_dBA[i]**2)
            
    for segment in q5.segments:
            for i in range(0,control_points):
                q5SPL.append(segment.conditions.noise.total_SPL_dBA[i]**2)
                
    for segment in q6.segments:
            for i in range(0,control_points):
                q6SPL.append(segment.conditions.noise.total_SPL_dBA[i]**2)
                
    for segment in q7.segments:
            for i in range(0,control_points):
                q7SPL.append(segment.conditions.noise.total_SPL_dBA[i]**2)
                
    for segment in q8.segments:
            for i in range(0,control_points):
                q8SPL.append(segment.conditions.noise.total_SPL_dBA[i]**2)
                
    for segment in q9.segments:
            for i in range(0,control_points):
                q9SPL.append(segment.conditions.noise.total_SPL_dBA[i]**2)
                         
            
    fullSPL = np.zeros((len(q1SPL),3*N_gm_x,3*N_gm_y))  
    for i in range(0,len(q1SPL)):
       
        fullSPL[i,0:N_gm_y,0:N_gm_x] =q1SPL[i].reshape(N_gm_x,N_gm_y, order = "F")
        fullSPL[i,N_gm_y:2*N_gm_y,0:N_gm_x] = q2SPL[i].reshape(N_gm_x,N_gm_y, order = "F")
        fullSPL[i,2*N_gm_y:,0:N_gm_x] = q3SPL[i].reshape(N_gm_x,N_gm_y, order = "F")
        fullSPL[i,0:N_gm_y,N_gm_x:2*N_gm_x]  = q4SPL[i].reshape(N_gm_x,N_gm_y, order = "F")
        fullSPL[i,N_gm_y:2*N_gm_y,N_gm_x:2*N_gm_x]  = q5SPL[i].reshape(N_gm_x,N_gm_y, order = "F")    
        fullSPL[i,2*N_gm_y:,N_gm_x:2*N_gm_x]  = q6SPL[i].reshape(N_gm_x,N_gm_y, order = "F") 
        fullSPL[i,0:N_gm_y,2*N_gm_x:]  = q7SPL[i].reshape(N_gm_x,N_gm_y, order = "F") 
        fullSPL[i,N_gm_y:2*N_gm_y,2*N_gm_x:]  = q8SPL[i].reshape(N_gm_x,N_gm_y, order = "F") 
        fullSPL[i,2*N_gm_y:,2*N_gm_x:]  = q8SPL[i].reshape(N_gm_x,N_gm_y, order = "F") 
        
        
    return fullSPL, micro

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
    print('Optimiser input :turn to base ',turn_to_base)
    print('Optimiser input:turn to final',turn_to_final)

    return mission