'''
This python code generates figure S5 in the appendix.
'''

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
queueDest = [list(range(2,8,1)),list(range(8,14,1)),list(range(14,20,1)),list(range(20,26,1))]
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
all_files = {}
# get files with WtW 0
all_files['0'] = glob.glob(parent_dir+'/data/2750pax_large/*')
# get files wih WtW 25
all_files['25'] = glob.glob(parent_dir+'/data/2750pax_large_WtW25/*')
# get files wih WtW 50
all_files['50'] = glob.glob(parent_dir+'/data/2750pax_large_WtW50/*')
# get files wih WtW 75
all_files['75'] = glob.glob(parent_dir+'/data/2750pax_large_WtW75/*')
# get files wih WtW 100
all_files['100'] = glob.glob(parent_dir+'/data/2750pax_large_WtW100/*')

numFile = 100
WtW = [0, 25, 50, 75, 100]
paxInfo = [all_files, numFile,queueDest,WtW]

# elevator
elevNumTotal = 14 # total number of elevators
elevSpeed = 1.4 # speed of elevator to traverse one floor
elevSpeedMultiplier = 1.3 # multiplier to account for intermediate pax entering and leaving
elevBoardTime = [15, 17, 19, 21] # time to board an elevator, depends on num of pax entering
elevStopTime = [15, 17, 19, 21] # time to unboard an elevator, depends on num of pax leaving
elevServiceRange = dict.fromkeys(range(elevNumTotal),list(range(2,26,1)))
elevCap = 4
elevInfo = [numFloor, elevNumTotal,elevSpeed,elevSpeedMultiplier, elevBoardTime, elevStopTime, elevServiceRange, elevCap]
IntervList = ["CohortFCFS"]
resultCap4 = run_compareInterv(paxInfo, elevInfo, IntervList)
 

############
## run Allocation 4 intervention
numFloor = 24
queueDest = [list(range(2,8,1)),list(range(8,14,1)),list(range(14,20,1)),list(range(20,26,1))]
elevServiceRange = dict.fromkeys(range(elevNumTotal),[])
for elev in [0,1,2]:
    elevServiceRange[elev] = list(range(2,8,1))
for elev in [3,4,5]:
    elevServiceRange[elev] = list(range(8,14,1))
for elev in [6,7,8,9]:
    elevServiceRange[elev] = list(range(14,20,1))
for elev in [10,11,12,13]:
    elevServiceRange[elev] = list(range(20,26,1))  
    
paxInfo = [all_files, numFile,queueDest,WtW]

# elevator

elevInfo = [numFloor, elevNumTotal,elevSpeed,elevSpeedMultiplier, elevBoardTime, elevStopTime, elevServiceRange, elevCap]

IntervList = ["Split4"]
resultAllocation = run_compareInterv(paxInfo, elevInfo, IntervList)



"Plot"

qList = [0, 25, 50, 75, 100]
policyList = ["CohortFCFS","Split4"]
data0 =[ [resultCap4["Queue"][q][policyList[0]][index][0] for index in range(numFile)] for q in qList]

# data1 = [ [resultCap4["Queue"][q][policyList[1]][index][0] for index in range(numFile)] for q in qList]
data6 = [ [resultAllocation["Queue"][q][policyList[1]][index][0] for index in range(numFile)] for q in qList]

ticks = [0, 25, 50, 75 , 100]

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)
    
plt.figure(figsize=(6, 4))

# bp1 = plt.boxplot(data0[0], positions=[-1], sym='', widths=0.25)
bp2 = plt.boxplot(data0, positions=np.array(range(len(data0)))*3.0-0.2, sym='', widths=0.3)
bp7 = plt.boxplot(data6, positions=np.array(range(len(data0)))*3.0+0.2, sym='', widths=0.3)

set_box_color(bp2, "red")
set_box_color(bp7, "gold")

# draw temporary red and blue lines and use them to create a legend
# plt.plot([], c= "black", label='FCFS')
plt.plot([], c="red", label='Cohorting')
plt.plot([], c="green", label='Allocation 4')
plt.legend(fontsize = 16)

plt.xticks( range(0, len(ticks) * 3, 3), ticks, fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlim(-1, len(ticks)*3-2)
plt.ylim(5, 45)
plt.tight_layout()

plt.xlabel("Willingness to Walk (in %)", fontsize = 16 )
plt.ylabel("Average Queue Length", fontsize = 16 )
# plt.title("Performance across 100 random scenarios\n Elevator Capacity = 4, Around 5500 passengers between 8am-10am", fontsize = 14 )
plt.show()

