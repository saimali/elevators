from matplotlib import pyplot as plt
import pandas as pd
import numpy as np
import random
import math
import csv
from collections import Counter
import itertools
import copy
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

######################################
# Try to cohort up to 4 passengers
WtW = 0
intervention ='CohortFCFS'
result = [[],[]]
lobbySizeRange = [2,4,6,8,10,12,14,16,20,30]
for lobbySize in lobbySizeRange:
    (waitTime,avgLowWaitTime,avgHighWaitTime,avgqueue,timequeue,load,tripTime,buttonPresses, avgEachQueue,timeEachQueue) = run_interventionOnMultipleFiles_LimitedCohort(paxInfo, elevInfo, intervention, lobbySize, 4)

    ResultWaitTime = list(waitTime)
    # round wait time to nearest second. however 4.5 will be rounded to 4, the nearest even number
    waitTime = [int(np.rint(number)) for number in waitTime]
    # round trip time to the nearest second. however 4.5 will be rounded to 4, the nearest even number
    tripTime = [int(np.rint(number)) for number in tripTime]
    result[0].append( truncate(np.average(ResultWaitTime),2))
    result[1].append(truncate(np.average(list(avgqueue)),2))

    
######################################  
# only cohorting 2 passengers together

intervention ='CohortFCFS'
result2 = [[],[]]
for lobbySize in lobbySizeRange:
    (waitTime,avgLowWaitTime,avgHighWaitTime,avgqueue,timequeue,load,tripTime,buttonPresses,
     avgEachQueue,timeEachQueue) = run_interventionOnMultipleFiles_LimitedCohort(paxInfo, elevInfo, intervention,lobbySize,2)

    ResultWaitTime = list(waitTime)
    # round wait time to nearest second. however 4.5 will be rounded to 4, the nearest even number
    waitTime = [int(np.rint(number)) for number in waitTime]
    # round trip time to the nearest second. however 4.5 will be rounded to 4, the nearest even number
    tripTime = [int(np.rint(number)) for number in tripTime]
    result2[0].append( truncate(np.average(ResultWaitTime),2))
    result2[1].append(truncate(np.average(list(avgqueue)),2))
    
    
########################################
# only cohorting 2 passengers without the lobby size constraint
intervention ='CohortFCFS'
result2limit2 = [[],[]]
for lobbySize in [200]:
    (waitTime,avgLowWaitTime,avgHighWaitTime,avgqueue,timequeue,load,tripTime,buttonPresses,
     avgEachQueue,timeEachQueue) = run_interventionOnMultipleFiles_LimitedCohort(paxInfo, elevInfo, intervention,lobbySize,2)

    ResultWaitTime = list(waitTime)
    # round wait time to nearest second. however 4.5 will be rounded to 4, the nearest even number
    waitTime = [int(np.rint(number)) for number in waitTime]
    # round trip time to the nearest second. however 4.5 will be rounded to 4, the nearest even number
    tripTime = [int(np.rint(number)) for number in tripTime]
    result2limit2[0].append( truncate(np.average(ResultWaitTime),2))
    result2limit2[1].append(truncate(np.average(list(avgqueue)),2))

#########################################
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo,"CohortFCFS")
ResultQueue = list(avgqueue)
benchmark1 = truncate(np.average(ResultQueue),2)

#########################################
(waitTime,avgqueue,timequeue,load,tripTime,buttonPresses,avgEachQueue,timeEachQueue) = run_InterventionOnMultipleFiles(paxInfo, elevInfo,'FCFS')
ResultQueue = list(avgqueue)
benchmark2 = truncate(np.average(ResultQueue),2)

########################################
## plot the queue length
plt.figure(figsize=(9, 6))
plt.plot(lobbySizeRange, result[1],'^-',linewidth=2, color = 'orange', label = "Cohorting in limited space")
plt.plot(lobbySizeRange[-1]+0.4, [benchmark1], 'o',linewidth=4, color = 'red', label = "Cohorting")

plt.plot(lobbySizeRange, result2[1],'^-',linewidth=2,color = 'purple', label = "Pairing in limited space")
plt.plot(lobbySizeRange[-1]+0.4, [result2limit2[1][0]],'o', color = 'magenta', linewidth=4, label = "Pairing")
plt.plot(lobbySizeRange[0]-0.4, [benchmark2], 'o',linewidth=4, color = 'black', label = "FCFS")

plt.xlabel('Number of passengers within reach of the Queue Manager', fontsize = 16)
plt.ylabel('Average Queue Length', fontsize = 16)
plt.xticks(lobbySizeRange, fontsize = 14)
plt.yticks( fontsize = 14)
plt.legend( fontsize = 16)#, loc = (1.01,0.25) )
# plt.ylim([10,30])
plt.show()