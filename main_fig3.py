"""
This python code generates figure 3 in the paper.
"""
# Notation for comments: pax <- passenger

from matplotlib import pyplot as plt

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
# put together all pax configurations
paxInfo = [all_files,numFile,queueDest,WtW]


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

"Compute results of 2 Queue Split"
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
waitTime_FCFSQueueSpliteven_2Q = waitTime
avgqueue_FCFSQueueSpliteven_2Q = avgqueue
timequeue_FCFSQueueSpliteven_2Q = timequeue
timeEachQueue_FCFSQueueSpliteven_2Q = timeEachQueue


"Compute results of 3 Queue Split"
intervention = "FCFSQueueSplit"
# set the floor ranges for each queue, here it is 3 queue split
queueDest = [list(range(2,10,1)),list(range(10,18,1)),list(range(18,26,1))]
# update paxInfo
paxInfo[2] = queueDest 
# run the intervention
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

# create list of wait time
ResultWaitTime = list(waitTime)
# round wait time to nearest second. 
waitTime = [int(np.rint(number)) for number in waitTime]

# store results
waitTime_FCFSQueueSpliteven_3Q = waitTime
avgqueue_FCFSQueueSpliteven_3Q = avgqueue
timequeue_FCFSQueueSpliteven_3Q = timequeue
timeEachQueue_FCFSQueueSpliteven_3Q = timeEachQueue

"Compute results of 4 Queue Split"
intervention = "FCFSQueueSplit"
# set the floor ranges for each queue, here it is 4 queue split
queueDest = [list(range(2,8,1)),list(range(8,14,1)),list(range(14,20,1)),list(range(20,26,1))]
# update paxInfo
paxInfo[2] = queueDest 
# run the intervention
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention)

# create list of wait time
ResultWaitTime = list(waitTime)
# round wait time to nearest second. 
waitTime = [int(np.rint(number)) for number in waitTime]

# store results
waitTime_FCFSQueueSpliteven_4Q = waitTime
avgqueue_FCFSQueueSpliteven_4Q = avgqueue
timequeue_FCFSQueueSpliteven_4Q = timequeue
timeEachQueue_FCFSQueueSpliteven_4Q = timeEachQueue

"Plot comparing interventions- creates one graph"
# queue length in the lobby vs time
fig = plt.figure()
ax = plt.subplot(1,1,1)
d = list(timequeue_FCFSQueueSpliteven_2Q)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='blue',label='2 Queue Split')
d = list(timequeue_FCFSQueueSpliteven_3Q)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='cyan',label ='3 Queue Split')
d = list(timequeue_FCFSQueueSpliteven_4Q)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='teal',label='4 Queue Split')
d = list(timequeue_CohortFCFS)
plt.plot(list(range(0,timeInterval*len(d), timeInterval)), d,color='red',label='Cohorting')
plt.xticks([0,1800,3600,5400,7100],['8:00 AM', '8:30 AM','9:00 AM','9:30 AM','10:00 AM'])
plt.xlim(-50,7101)
plt.xlabel('Time')
plt.ylabel('Queue Length in the lobby')
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
ax.spines['right'].set_visible(False)
ax.spines['top'].set_visible(False)
ax.legend(loc='center left', bbox_to_anchor=(1,0.5),fontsize='x-large',shadow=True, fancybox=True)
