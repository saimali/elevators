"""
This python code generates figure S2 (appendix) in the paper.
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
# round trip time to the nearest second. 
tripTime = [int(np.rint(number)) for number in tripTime]

# store results
waitTime_FCFS = waitTime
avgqueue_FCFS = avgqueue
timequeue_FCFS = timequeue
load_FCFS = load
tripTime_FCFS = tripTime
buttonPresses_FCFS = buttonPresses

"Compute results of Cohorting"
intervention = "CohortFCFS"
# run the intervention
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

# create list of wait time
ResultWaitTime = list(waitTime)
# round wait time to nearest second. 
waitTime = [int(np.rint(number)) for number in waitTime]
# round trip time to the nearest second. 
tripTime = [int(np.rint(number)) for number in tripTime]

# store results
waitTime_CohortFCFS = waitTime
avgqueue_CohortFCFS = avgqueue
timequeue_CohortFCFS = timequeue
load_CohortFCFS = load
tripTime_CohortFCFS = tripTime
buttonPresses_CohortFCFS = buttonPresses


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
# round trip time to the nearest second. 
tripTime = [int(np.rint(number)) for number in tripTime]

# store results
waitTime_FCFSQueueSplit = waitTime
avgqueue_FCFSQueueSplit = avgqueue
timequeue_FCFSQueueSplit = timequeue
load_FCFSQueueSplit = load
tripTime_FCFSQueueSplit = tripTime
buttonPresses_FCFSQueueSplit = buttonPresses


"Plots comparing interventions- creates a 1 row 3 column plot"

# fig = plt.figure(figsize=(15,5))
# # histogram of waiting time of pax
# plt.subplot(1, 3, 1)
fig = plt.figure(figsize=(15, 5))
ax = plt.subplot(1, 3, 1)
elevLoadBin=[]
for i in np.arange(0,4+1,1):
    elevLoadBin+= [i-0.5, i+0.5 ]
common_params = dict(bins=elevLoadBin, 
                     range=(1, 4))
# plt.hist(load_FCFS,**common_params,color='black')
# plt.hist(load_CohortFCFS,**common_params,color='red')
plt.hist([load_FCFS, load_CohortFCFS,load_FCFSQueueSplit], **common_params,alpha=0.7,
         rwidth=None, color=['black','red','blue'],density=True,label=['Default FCFS','Cohorting','2 Queue Split'])
plt.xticks(list(range(1,elevCap+1)))
plt.xlim(xmin = 0.5, xmax = elevCap+0.5)
plt.xlabel('Number of Passengers (load) per elevator trip')
plt.ylabel('Percentage of elevator trip')
y_value=['{:.0f}'.format(1e2*x) + '%' for x in ax.get_yticks()]
ax.set_yticklabels(y_value)
#plt.title('Load Histogram')
plt.legend(loc='upper left', bbox_to_anchor=(0,1),fontsize='x-large',shadow=True, fancybox=True)
ax.text(-0.1, 1.1,'A', transform=ax.transAxes, 
            size=20, weight='bold')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
# trip time of pax

# fig = plt.figure(figsize=(15,5))
# # histogram of waiting time of pax
# plt.subplot(1, 3, 1)
ax = plt.subplot(1, 3, 2)
# d = list(tripTime_FCFS)
# n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 5), color='black',
#                             alpha=0.5, density=True, rwidth=None, label='Default FCFS')

# d = list(tripTime_CohortFCFS)
# n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 5), color='red',
#                             alpha=0.5, density=True, rwidth=None, label='Cohorting')

# d = list(tripTime_FCFSQueueSplit)
# n, bins, patches = plt.hist(x=d, bins=range(min(d), max(d) +1, 5), color='blue',
#                             alpha=0.2, density=True, rwidth=None, label='2 Queue Split')

common_params = dict(bins=range(0,130,25),range=(0,130,25))
                     #, range=(1, 4)) 
plt.hist([tripTime_FCFS, tripTime_CohortFCFS,tripTime_FCFSQueueSplit], **common_params,alpha=0.7,
         rwidth=None, color=['black','red','blue'],density=True,label=['Default FCFS','Cohorting','2 Queue Split'])
plt.xticks(list(range(25,130,25)))

plt.xlim(xmin = 25, xmax = 130)

y_value=['{:.0f}'.format(1e3*x*2.5) + '%' for x in ax.get_yticks()]
ax.set_yticklabels(y_value)
#ax.set_yticklabels(['0%','10%','20%','30%','40%'])
#plt.xticks(np.arange(0,300,10))
#plt.ylim(ymin=0,ymax=0)
plt.ylabel('Percentage of Passengers')
plt.xlabel('Trip time of passengers in elevators (seconds)')
ax.text(-0.1, 1.1,'B', transform=ax.transAxes, 
            size=20, weight='bold')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#plt.legend(loc='upper right', bbox_to_anchor=(1,1),fontsize='x-large',shadow=True, fancybox=True)



# ax = plt.subplot(1, 3, 2)
# llim=25
# ulim=2699
# step=20
# timeInterval=10 # we update the system every 10 seconds
# d = list(tripTime_FCFS[llim:ulim:step])
# plt.plot(list(range(llim,ulim,step)), d,color='black',label='Default FCFS')
# d = list(tripTime_CohortFCFS[llim:ulim:step])
# plt.plot(list(range(llim,ulim,step)), d,color='red',label ='Cohorting')
# d = list(tripTime_FCFSQueueSplit[llim:ulim:step])
# plt.plot(list(range(llim,ulim,step)), d,color='blue',label='2 Queue Split')
# #plt.xticks([0,1800,3600,5400,7100],['8:00 AM', '8:30 AM','9:00 AM','9:30 AM','10:00 AM'])
# plt.ylim(ymin=50,ymax=90)
# plt.xlabel('Passenger Index (in order of arrival)')
# plt.ylabel('Trip Time (s)')
# #plt.title('Elevator Trip Time of Passengers')
# ax.text(-0.1, 1.1,'B', transform=ax.transAxes, 
#             size=20, weight='bold')
# ax.spines['right'].set_visible(False)
# ax.spines['top'].set_visible(False)
# #plt.legend(loc='upper left', bbox_to_anchor=(0,1),fontsize='x-large', shadow=True, fancybox=True)
# # number of elevator stops


ax = plt.subplot(1, 3, 3)
elevStopBin=[]
for i in np.arange(0,4+1,1):
    elevStopBin+= [i-0.5, i+0.5 ]
common_params = dict(bins=elevStopBin, 
                     range=(1, 4))
# plt.hist(load_FCFS,**common_params,color='black')
# plt.hist(load_CohortFCFS,**common_params,color='red')
plt.hist([buttonPresses_FCFS, buttonPresses_CohortFCFS,buttonPresses_FCFSQueueSplit], **common_params,alpha=0.7,
         rwidth=None, color=['black','red','blue'],density=True,label=['Default FCFS','Cohorting','2 Queue Split'])
#plt.grid(axis='y', alpha=0.7)
y_value=['{:.0f}'.format(1e2*x) + '%' for x in ax.get_yticks()]
ax.set_yticklabels(y_value)
plt.xticks(list(range(1,elevCap+1)))
plt.xlim(xmin = 0.5, xmax = elevCap+0.5)
plt.xlabel('Number of Stops (button presses) per elevator trip')
plt.ylabel('Percentage of elevator trips')
ax.text(-0.1, 1.1,'C', transform=ax.transAxes, 
            size=20, weight='bold')
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
#plt.title('Number of Stops in elevator trips')
#plt.legend(loc='upper left', bbox_to_anchor=(0,1),fontsize='x-large',shadow=True, fancybox=True)

