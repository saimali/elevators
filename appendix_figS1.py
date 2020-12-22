"""
This python code generates figure S1 (appendix) in the paper.
"""

from matplotlib import pyplot as plt

import pandas as pd
import numpy as np
import random
import math
from collections import Counter
import itertools

"Small Sized building configuration"
# building information: floor 1-7, pax destination 2-6  
numFloor = 6 # total number of pax destinations
numPax = 400 # total number of pax during rush hour
timeInterval = 10 # we update the system every 10 seconds

# info for pax arrivals
# number of simulations
numFile = 100
# floor ranges of each queue if we are queue splitting, default []
queueDest = []
 #can be anything from 0 to 100- usually we do 0,20,40,60,80,100
WtW = 0 
# create arrival files, will be stored in the same folder we run the code
# if we want different random simulations, uncomment the lines below
""" 
createOtherArrivalFiles(numPax,numFloor,WtW,numFile)
fileName = str(numPax)+"_"+str(numFloor)+"_"+str(WtW)+"_"
"""
# name of the files used for the simulations, 
# these files will yield exactly the figures in the paper
# if we want new random files, comment the line below
# get current working directory
parent_dir = str(os.getcwd())
# get csv files in subdirectory for this setup   
all_files = glob.glob(parent_dir+'/data/400pax_small/*')
# put together all pax configurations
paxInfo = [all_files,numFile,queueDest,WtW]

# elevator info
# total number of elevators
elevNumTotal = 2
# speed of elevator to traverse one floor
elevSpeed = 1.4 
# multiplier to account for intermediate pax entering and leaving
elevSpeedMultiplier = 1.3 
# time to board an elevator, depends on num of pax entering the elev
# if there is one pax, they take 15s to board + 2s for every additional pax
elevBoardTime = [15, 17, 19, 21] 
# time to deboard an elevator, depends on num of pax exiting the elev
# if there is one pax, they take 15s to deboard + 2s for every additional pax
elevStopTime = [15, 17, 19, 21] 
# the range of floors the elev can serve, right now all elevs can serve all floors
elevServiceRange = dict.fromkeys(range(elevNumTotal),list(range(2,numFloor+2,1)))
# capacity of the elevators
elevCap = 2
# put together all elev configurations
elevInfo = [numFloor, elevNumTotal,elevSpeed,elevSpeedMultiplier, elevBoardTime, elevStopTime, elevServiceRange, elevCap]

"Compute results of FCFS"
intervention = "FCFS"
(_,_,timequeue,_,_,_,_,_) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

timequeue_FCFS_small = timequeue

"Compute results of Cohorting"
intervention = "CohortFCFS"
# run the intervention
(_,_,timequeue,_,_,_,_,_) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

timequeue_CohortFCFS_small = timequeue


"Compute results of 2 Queue Split"
intervention = "FCFSQueueSplit"
# set the floor ranges for each queue, here it is 2 queue split
queueDest = [list(range(2,5,1)),list(range(5,8,1))]
# update paxInfo
paxInfo[2] = queueDest 
# run the intervention
(_,_,timequeue,_,_,_,_,_) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

timequeue_FCFSQueueSpliteven_2Q_small = timequeue

"Compute results of 3 Queue Split"
intervention = "FCFSQueueSplit"
# set the floor ranges for each queue, here it is 2 queue split
queueDest = [list(range(2,4,1)),list(range(4,6,1)),list(range(6,8,1))]
# update paxInfo
paxInfo[2] = queueDest 
# run the intervention
(_,_,timequeue,_,_,_,_,_) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

timequeue_FCFSQueueSpliteven_3Q_small = timequeue

"""
"Medium Sized building configuration
"""

# building information: floor 1-16, pax destination 2-16  
numFloor = 15 # total number of pax destinations
numPax = 1500 # total number of pax during rush hour
timeInterval = 10 # we update the system every 10 seconds

# info for pax arrivals
# number of simulations
numFile = 100
# floor ranges of each queue if we are queue splitting, default []
queueDest = []
 #can be anything from 0 to 100- usually we do 0,20,40,60,80,100
WtW = 0 
# create arrival files, will be stored in the same folder we run the code
# if we want different random simulations, uncomment the lines below
""" 
createOtherArrivalFiles(numPax,numFloor,WtW,numFile)
fileName = str(numPax)+"_"+str(numFloor)+"_"+str(WtW)+"_"
"""
# name of the files used for the simulations, 
# these files will yield exactly the figures in the paper
# if we want new random files, comment the line below
# get current working directory
parent_dir = str(os.getcwd())
# get csv files in subdirectory for this setup   
all_files = glob.glob(parent_dir+'/data/1500pax_medium/*')
# put together all pax configurations
paxInfo = [all_files,numFile,queueDest,WtW]

# elevator info
# total number of elevators
elevNumTotal = 6
# speed of elevator to traverse one floor
elevSpeed = 1.4 
# multiplier to account for intermediate pax entering and leaving
elevSpeedMultiplier = 1.3 
# time to board an elevator, depends on num of pax entering the elev
# if there is one pax, they take 15s to board + 2s for every additional pax
elevBoardTime = [15, 17, 19, 21] 
# time to deboard an elevator, depends on num of pax exiting the elev
# if there is one pax, they take 15s to deboard + 2s for every additional pax
elevStopTime = [15, 17, 19, 21] 
# the range of floors the elev can serve, right now all elevs can serve all floors
elevServiceRange = dict.fromkeys(range(elevNumTotal),list(range(2,numFloor+2,1)))
# capacity of the elevators
elevCap = 4
# put together all elev configurations
elevInfo = [numFloor, elevNumTotal,elevSpeed,elevSpeedMultiplier, elevBoardTime, elevStopTime, elevServiceRange, elevCap]

"Compute results of FCFS"
intervention = "FCFS"
# run the intervention
(_,_,timequeue,_,_,_,_,_) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

timequeue_FCFS_medium = timequeue

"Compute results of Cohorting"
intervention = "CohortFCFS"
# run the intervention
(_,_,timequeue,_,_,_,_,_) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

timequeue_CohortFCFS_medium = timequeue



"Compute results of 2 Queue Split"
intervention = "FCFSQueueSplit"
# set the floor ranges for each queue, here it is 2 queue split
queueDest = [list(range(2,10,1)),list(range(10,17,1))]
# update paxInfo
paxInfo[2] = queueDest 
# run the intervention
(_,_,timequeue,_,_,_,_,_) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

timequeue_FCFSQueueSpliteven_2Q_medium = timequeue

"Compute results of 3 Queue Split"
intervention = "FCFSQueueSplit"
# set the floor ranges for each queue, here it is 2 queue split
queueDest = [list(range(2,7,1)),list(range(7,12,1)),list(range(12,17,1))]
# update paxInfo
paxInfo[2] = queueDest 
# run the intervention
(_,_,timequeue,_,_,_,_,_) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

timequeue_FCFSQueueSpliteven_3Q_medium = timequeue

"Compute results of 4 Queue Split"
intervention = "FCFSQueueSplit"
# set the floor ranges for each queue, here it is 2 queue split
queueDest = [list(range(2,6,1)),list(range(6,10,1)),list(range(10,14,1)),list(range(14,17,1))]
# update paxInfo
paxInfo[2] = queueDest 
# run the intervention
(_,_,timequeue,_,_,_,_,_) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

timequeue_FCFSQueueSpliteven_4Q_medium = timequeue

"Plots comparing interventions- creates a 1 row 2 column plot"
# queue length in the lobby vs time
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(1,2,1)
timeInterval=10 # we update the system every 10 seconds
d = list(timequeue_FCFS_small)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='black',label='Default FCFS')
d = list(timequeue_CohortFCFS_small)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='red',label ='Cohorting')
d = list(timequeue_FCFSQueueSpliteven_2Q_small)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='blue',label='2 Queue Split')
d = list(timequeue_FCFSQueueSpliteven_3Q_small)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='cyan',label='3 Queue Split')
plt.xticks([0,1800,3600,5400,7100],['8:00 AM', '8:30 AM','9:00 AM','9:30 AM','10:00 AM'])
plt.xlim(-50,7101)
plt.xlabel('Time')
plt.ylabel('Queue length in the lobby')
ax.text(-0.1, 1.1,'A', transform=ax.transAxes, 
            size=20, weight='bold')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.legend(loc='upper left', bbox_to_anchor=(0,1),fontsize='x-large',shadow=True, fancybox=True)


# queue length in the lobby vs time
ax = plt.subplot(1,2,2)
timeInterval=10 # we update the system every 10 seconds
d = list(timequeue_FCFS_medium)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='black',label='Default FCFS')
d = list(timequeue_CohortFCFS_medium)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='red',label ='Cohorting')
d = list(timequeue_FCFSQueueSpliteven_2Q_medium)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='blue',label='2 Queue Split')
d = list(timequeue_FCFSQueueSpliteven_3Q_medium)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='cyan',label='3 Queue Split')
d = list(timequeue_FCFSQueueSpliteven_4Q_medium)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='teal',label='4 Queue Split')

plt.xticks([0,1800,3600,5400,7100],['8:00 AM', '8:30 AM','9:00 AM','9:30 AM','10:00 AM'])
plt.xlim(-50,7101)
plt.xlabel('Time')
plt.ylabel('Queue length in the lobby')
ax.text(-0.1, 1.1,'B', transform=ax.transAxes, 
            size=20, weight='bold')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.legend(loc='upper left', bbox_to_anchor=(0,1),fontsize='x-large',shadow=True, fancybox=True)
