"""
This python code generates figure S3 (appendix) in the paper.
"""

from matplotlib import pyplot as plt

import pandas as pd
import numpy as np
import random
import math
from collections import Counter
import itertools
 
# building information: floor 1-25, pax destination 2-25   
numFloor = 24 # total number of pax destinations
numPax = 2750 # total number of pax during rush hour
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
all_files = glob.glob(parent_dir+'/data/2750pax_large/*')
# put together all pax configurations
paxInfo = [all_files,numFile,queueDest,WtW]

# elevator info
# total number of elevators
elevNumTotal = 14 
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
# the range of floors the elev can serve, the first 7 elevators serve floors 2-15
elevServiceRange = dict.fromkeys(range(7),list(range(2,14,1)))
# the next 7 elevators serve floors 16-25
for elev in range(7,14,1):
    set_key(elevServiceRange,elev,list(range(14,26,1)))
# capacity of the elevators
elevCap = 4
# put together all elev configurations
elevInfo = [numFloor, elevNumTotal,elevSpeed,elevSpeedMultiplier, elevBoardTime, elevStopTime, elevServiceRange, elevCap]


"Compute results of 4 Queue Split- equal split"
intervention = "FCFSQueueSplit"
# set the floor ranges for each queue, here it is 2 queue split
queueDest = [list(range(2,8,1)),list(range(8,14,1)),list(range(14,20,1)),list(range(20,26,1))]
# update paxInfo
paxInfo[2] = queueDest 
# run the intervention
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

# create list of wait time
ResultWaitTime = list(waitTime)
# round wait time to nearest second. 
waitTime = [int(np.rint(number)) for number in waitTime]
# round trip time to the nearest second. 
tripTime = [int(np.rint(number)) for number in tripTime]

# store results
waitTime_FCFSQueueSpliteven_4Q = waitTime
avgqueue_FCFSQueueSpliteven_4Q = avgqueue
timequeue_FCFSQueueSpliteven_4Q = timequeue
timeEachQueue_FCFSQueueSpliteven_4Q = timeEachQueue

"Compute results of 4 Queue Split- unequal split"
intervention = "FCFSQueueSplit"
# set the floor ranges for each queue, here it is 2 queue split
queueDest = [list(range(2,8,1)),list(range(8,14,1)),list(range(14,22,1)),list(range(22,26,1))]
# update paxInfo
paxInfo[2] = queueDest 
# run the intervention
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

# create list of wait time
ResultWaitTime = list(waitTime)
# round wait time to nearest second. 
waitTime = [int(np.rint(number)) for number in waitTime]
# round trip time to the nearest second. 
tripTime = [int(np.rint(number)) for number in tripTime]

# store results
waitTime_FCFSQueueSplitnoteven_4Q = waitTime
avgqueue_FCFSQueueSplitnoteven_4Q = avgqueue
timequeue_FCFSQueueSplitnoteven_4Q = timequeue
timeEachQueue_FCFSQueueSplitnoteven_4Q = timeEachQueue

"Plots"
"Length of diff queues if floor ranges split evenly"
# queue length of each queue in the lobby vs time
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(1,2,1)
timeInterval=10
d=timeEachQueue_FCFSQueueSpliteven_4Q 
queueDestLabels=['Floors 2-7', 'Floors 8-13','Floors 14-19','Floors 20-25']
colorList = ['orange','green','maroon','magenta']
for j in range(4): 
    ax.plot(list(range(0,timeInterval*len(d[j]), timeInterval)), list(d[j]),label=queueDestLabels[j],color=colorList[j])

# plt.xticks(np.arange(0,9000,1800))
plt.xticks([0,1800,3600,5400,7100],['8:00 AM', '8:30 AM','9:00 AM','9:30 AM','10:00 AM'])
plt.xlim(-50,7101)
plt.xlabel('Time')
plt.ylabel('Queue Length in the lobby')
#plt.title('Length of Each Queue', y = -0.25)
plt.ylim(ymin = 0)        
ax.text(-0.1, 1.1,'A', transform=ax.transAxes, 
            size=20, weight='bold')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
plt.legend(loc='upper left', bbox_to_anchor=(0,1),fontsize='x-large',shadow=True, fancybox=True)

# Put a legend to the right of the current axis
#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize='x-large')


"Plots"
"Length of diff queues if floor ranges split UNevenly"
# queue length of each queue in the lobby vs time
ax = plt.subplot(1,2,2)
timeInterval=10
d=timeEachQueue_FCFSQueueSplitnoteven_4Q 
queueDestLabels=['Floors 2-7', 'Floors 8-13','Floors 14-21','Floors 22-25']
colorList = ['orange','green','maroon','magenta']
for j in range(4): 
    ax.plot(list(range(0,timeInterval*len(d[j]), timeInterval)), list(d[j]),label=queueDestLabels[j],color=colorList[j])

# plt.xticks(np.arange(0,9000,1800))
plt.xticks([0,1800,3600,5400,7100],['8:00 AM', '8:30 AM','9:00 AM','9:30 AM','10:00 AM'])
plt.xlim(-50,7101)
plt.xlabel('Time')
plt.ylabel('Queue Length in the lobby')
#plt.title('Length of Each Queue', y = -0.25)
plt.ylim(ymin = 0,ymax=64)   
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.text(-0.1, 1.1,'B', transform=ax.transAxes, 
            size=20, weight='bold')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# Put a legend to the right of the current axis
#ax.legend(loc='center left', bbox_to_anchor=(1, 0.5),fontsize='x-large')
plt.legend(loc='upper left', bbox_to_anchor=(0,1),fontsize='x-large',shadow=True, fancybox=True)





# "Compute results of FCFS"
# intervention = "FCFS"
# # run the intervention
# (waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

# # create list of wait time
# ResultWaitTime = list(waitTime)
# # round wait time to nearest second. 
# waitTime = [int(np.rint(number)) for number in waitTime]
# # round trip time to the nearest second. 
# tripTime = [int(np.rint(number)) for number in tripTime]

# # store results
# waitTime_FCFS = waitTime
# avgqueue_FCFS = avgqueue
# timequeue_FCFS = timequeue

# "Compute results of Cohorting"
# intervention = "CohortFCFS"
# # run the intervention
# (waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

# # create list of wait time
# ResultWaitTime = list(waitTime)
# # round wait time to nearest second. 
# waitTime = [int(np.rint(number)) for number in waitTime]
# # round trip time to the nearest second. 
# tripTime = [int(np.rint(number)) for number in tripTime]

# # store results
# waitTime_CohortFCFS = waitTime
# avgqueue_CohortFCFS = avgqueue
# timequeue_CohortFCFS = timequeue

# timeInterval=10 # we update the system every 10 seconds
# d = list(timequeue_FCFS)
# plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='black',label='Default FCFS')
# d = list(timequeue_CohortFCFS)
# plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='red',label ='Cohorting')
# # d = list(timequeue_FCFSQueueSplit)
# # plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='blue',label='2 Queue Split')
# plt.xticks([0,1800,3600,5400,7100],['8:00 AM', '8:30 AM','9:00 AM','9:30 AM','10:00 AM'])
# plt.xlim(-50,7101)
# plt.xlabel('Time')
# plt.ylabel('Queue Length')
# plt.title('Queue Length vs Time')
# plt.legend(loc='upper left', bbox_to_anchor=(0,1),fontsize='x-large', shadow=True, fancybox=True)

# plt.show()
