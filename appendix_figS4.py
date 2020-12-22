"""
This python code generates figure S4 (appendix) in the paper
"""

from matplotlib import pyplot as plt
from matplotlib.ticker import PercentFormatter
import matplotlib.ticker as ticker

import pandas as pd
import numpy as np
import random
import math
from collections import Counter
import itertools
import os
import glob
import string

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
#        fileName = "2750_nowalk_0__"
# put together all pax configurations
#       paxInfo = [fileName,numFile,queueDest,WtW]
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
# the range of floors the elev can serve, right now all elevs can serve all floors
elevServiceRange = dict.fromkeys(range(elevNumTotal),list(range(2,numFloor+2,1)))
# capacity of the elevators
elevCap = 4
# put together all elev configurations
elevInfo = [numFloor, elevNumTotal,elevSpeed,elevSpeedMultiplier, elevBoardTime, elevStopTime, elevServiceRange, elevCap]


"Compute results of FCFS"
intervention = "FCFS"
# run the intervention
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)
# create list of wait time
ResultWaitTime = list(waitTime)
# round wait time to nearest second. 
waitTime = [int(np.rint(number)) for number in waitTime]

# store results
waitTime_FCFS = waitTime
avgqueue_FCFS = avgqueue
timequeue_FCFS = timequeue

"Compute results of Cohorting"
intervention = "CohortFCFS"
# run the intervention
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

# create list of wait time
ResultWaitTime = list(waitTime)
# round wait time to nearest second. 
waitTime = [int(np.rint(number)) for number in waitTime]

# store results
waitTime_CohortFCFS = waitTime
avgqueue_CohortFCFS = avgqueue
timequeue_CohortFCFS = timequeue



"Compute results of Queue Split"
intervention = "FCFSQueueSplit"
# set the floor ranges for each queue, here it is 2 queue split
queueDest = [list(range(2,14,1)),list(range(14,26,1))]
# update paxInfo
paxInfo[2] = queueDest 
# run the intervention
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

# create list of wait time
ResultWaitTime = list(waitTime)
# round wait time to nearest second. 
waitTime = [int(np.rint(number)) for number in waitTime]

# store results
waitTime_FCFSQueueSplit = waitTime
avgqueue_FCFSQueueSplit = avgqueue
timequeue_FCFSQueueSplit = timequeue


"Compute results of Allocation"
intervention = "FCFSSplit2"

elevServiceRange = dict.fromkeys(range(elevNumTotal),[])
for elev in [0,1,2,3,4,5,6]:
    elevServiceRange[elev] = list(range(2,14,1))
for elev in [7,8,9,10,11,12,13]:
    elevServiceRange[elev] = list(range(14,26,1))
    

# set the floor ranges for each queue, here it is 2 queue split
queueDest = [list(range(2,14,1)),list(range(14,26,1))]
# update paxInfo
paxInfo[2] = queueDest 
# update elevInfo
elevInfo[6] = elevServiceRange 
# run the intervention
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

# create list of wait time
ResultWaitTime = list(waitTime)
# round wait time to nearest second. 
waitTime = [int(np.rint(number)) for number in waitTime]

# store results
waitTime_Allocation2 = waitTime
avgqueue_Allocation2= avgqueue
timequeue_Allocation2 = timequeue


"Compute results of Allocation"
intervention = "FCFSSplit4"

elevServiceRange = dict.fromkeys(range(elevNumTotal),[])
for elev in [0,1,2]:
    elevServiceRange[elev] = list(range(2,8,1))
for elev in [3,4,5]:
    elevServiceRange[elev] = list(range(8,14,1))
for elev in [6,7,8,9]:
    elevServiceRange[elev] = list(range(14,20,1))
for elev in [10,11,12,13]:
    elevServiceRange[elev] = list(range(20,26,1))    

# set the floor ranges for each queue, here it is 2 queue split
queueDest = [list(range(2,14,1)),list(range(14,26,1))]
# update paxInfo
paxInfo[2] = queueDest 
# update elevInfo
elevInfo[6] = elevServiceRange 
# run the intervention
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

# create list of wait time
ResultWaitTime = list(waitTime)
# round wait time to nearest second. 
waitTime = [int(np.rint(number)) for number in waitTime]

# store results
waitTime_Allocation4 = waitTime
avgqueue_Allocation4 = avgqueue
timequeue_Allocation4 = timequeue

###########################################
"Plots comparing interventions- creates a 1 row 3 column plot"
fig = plt.figure(figsize=(15, 5))
# histogram of waiting time of pax
ax = plt.subplot(1, 3, 1)
d = list(waitTime_FCFS)
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 10), color='black',
                            alpha=0.7, density=True, rwidth=None, label='Default FCFS')

d = list(waitTime_CohortFCFS)
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 10), color='red',
                            alpha=0.7, density=True, rwidth=None, label='Cohorting')

d = list(waitTime_FCFSQueueSplit)
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 10), color='blue',
                            alpha=0.7, density=True, rwidth=None, label='2 Queue Split')

d = list(waitTime_Allocation2)
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 10), color='green',
                            alpha=0.7, density=True, rwidth=None, label='Allocation 2')

d = list(waitTime_Allocation4)
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 10), color='gold',
                            alpha=0.7, density=True, rwidth=None, label='Allocation 4')

y_value=['{:.0f}'.format(1e3*x) + '%' for x in ax.get_yticks()]
ax.set_yticklabels(y_value)
plt.xticks(np.arange(0,500,50))
plt.ylabel('Percentage of Passengers')
plt.xlabel('Waiting Time (seconds)')
ax.text(-0.1, 1.1,'A', transform=ax.transAxes, 
            size=20, weight='bold')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.legend(loc='upper right', bbox_to_anchor=(1,1),fontsize='x-large',shadow=True, fancybox=True)

# histogram of queue length in the lobby
ax = plt.subplot(1, 3, 2)
d = list(avgqueue_FCFS)
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 10), color='black',
                            alpha=0.7,density=True, rwidth=None,label='Default FCFS')
d = list(avgqueue_CohortFCFS)
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 10), color='red',
                            alpha=0.7,density=True, rwidth=None, label ='Cohorting')
d = list(avgqueue_FCFSQueueSplit)
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 10), color='blue',
                            alpha=0.7,density=True, rwidth=None, label='2 Queue Split')

d = list(avgqueue_Allocation2)
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 10), color='green',
                            alpha=0.7,density=True, rwidth=None, label='Allocation 2')

d = list(avgqueue_Allocation4)
n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 10), color='gold',
                            alpha=0.7,density=True, rwidth=None, label='Allocation 4')

y_value=['{:.0f}'.format(1e3*x) + '%' for x in ax.get_yticks()]
ax.set_yticklabels(y_value)
plt.xticks(np.arange(0,250,50))
plt.xlabel('Queue Length in the lobby measured every 10s')
plt.ylabel('Percentage of time')
ax.text(-0.1, 1.1,'B', transform=ax.transAxes, 
            size=20, weight='bold')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#plt.legend(loc='upper right', bbox_to_anchor=(1,1),fontsize='x-large',shadow=True, fancybox=True)

# queue length in the lobby vs time
ax = plt.subplot(1, 3, 3)
timeInterval=10 # we update the system every 10 seconds
d = list(timequeue_FCFS)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='black',label='Default FCFS')
d = list(timequeue_CohortFCFS)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='red',label ='Cohorting')
d = list(timequeue_FCFSQueueSplit)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='blue',label='2 Queue Split')
d = list(timequeue_Allocation2)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='green',label='Allocation 2')
d = list(timequeue_Allocation4)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='gold',label='Allocation 4')

plt.xticks([0,1800,3600,5400,7100],['8:00 AM', '8:30 AM','9:00 AM','9:30 AM','10:00 AM'])
plt.xlim(-50,7101)
plt.xlabel('Time')
plt.ylabel('Queue Length in the lobby')
#plt.title('Queue Length vs Time')
#plt.legend(loc='upper left', bbox_to_anchor=(0,1),fontsize='x-large', shadow=True, fancybox=True)
ax.text(-0.1, 1.1,'C', transform=ax.transAxes, 
            size=20, weight='bold')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
plt.show()
