
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
    q5Grid = q5.segments[0].analyses.noise.settings.ground_microphone_locations
    q6Grid = q6.segments[0].analyses.noise.settings.ground_microphone_locations
    q7Grid = q7.segments[0].analyses.noise.settings.ground_microphone_locations
    q8Grid = q8.segments[0].analyses.noise.settings.ground_microphone_locations
    q9Grid = q9.segments[0].analyses.noise.settings.ground_microphone_locations
    
    gridX = np.concatenate((q1Grid[:, 0], q2Grid[:, 0], q3Grid[:, 0], q4Grid[:, 0],q5Grid[:, 0],q6Grid[:, 0],q7Grid[:, 0],q8Grid[:, 0],q9Grid[:, 0]))
    gridY = np.concatenate((q1Grid[:, 1], q2Grid[:, 1], q3Grid[:, 1], q4Grid[:, 1],q5Grid[:, 1],q6Grid[:, 1],q7Grid[:, 1],q8Grid[:, 1],q9Grid[:, 1]))
    
    
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
                q1SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                
    for segment in q2.segments:
            for i in range(0,control_points):
                q2SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                
    for segment in q3.segments:
            for i in range(0,control_points):
                q3SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                
    for segment in q4.segments:
            for i in range(0,control_points):
                q4SPL.append(segment.conditions.noise.total_SPL_dBA[i])
            
    for segment in q5.segments:
            for i in range(0,control_points):
                q5SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                
    for segment in q6.segments:
            for i in range(0,control_points):
                q6SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                
    for segment in q7.segments:
            for i in range(0,control_points):
                q7SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                
    for segment in q8.segments:
            for i in range(0,control_points):
                q8SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                
    for segment in q9.segments:
            for i in range(0,control_points):
                q9SPL.append(segment.conditions.noise.total_SPL_dBA[i])
                         
                    
                
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
        fullSPL[i,2*N_gm_y:,2*N_gm_x:]  = q9SPL[i].reshape(N_gm_x,N_gm_y, order = "F") 
        
        
        
    X,Y, splData = gridSetup(N_gm_x, N_gm_y, gridX, gridY, fullSPL)
    
    
    #plotting function calls
    groundTrackplot(trajectory,gridX,gridY)
    dBA_max_plot(X,Y,splData,trajectory)
    #timeStepPlot(X, Y, splData,5)
    #cool3dPlot(X, Y, splData,trajectory)






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
    
    plt.savefig('Groundplot'+'.pdf')

    return 

    
def gridSetup(N_gm_x,N_gm_y,mx,my,zVals):
  
    sizeX =int( math.sqrt( N_gm_x**2 * 4))
    sizeY =int( math.sqrt(N_gm_y**2 * 4))
    
    mx = np.sort(mx)
    my = np.sort(my)
    
    
    X = []
    for i in range(0,len(mx),N_gm_x*3):
        X.append(mx[i])
        
    Y = []
    for i in range(0,len(my),N_gm_x*3):
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

def dBA_max_plot(X,Y,zVals,trajectory):
    
    maxdBA = np.nanmax(zVals, axis = 0)
    fig, ax = plt.subplots()

    # Set x and y axis limits
    ax.set_xlim([np.min(X), np.max(X)])
    ax.set_ylim([np.min(Y), np.max(Y)])
    
    # Set up color map
    levs   = np.linspace(30,50,40)
    im = ax.contourf(X , Y,maxdBA, levels = levs,  cmap=plt.cm.jet, extend='max') 
    ax.scatter(trajectory[:,0], trajectory[:,1], color='Black')
    ax.set_title('microphone maximum dBAs')
    cbar = fig.colorbar(im, ax=ax)
    cbar.ax.set_ylabel('max dBA')
        
        # Show plot
    plt.show()
    plt.savefig(f'dbaplot'+'.pdf')
    return



resultProcessing()