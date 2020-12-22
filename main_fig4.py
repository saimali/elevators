"""
This python code generates figure 4 in paper.
"""
# Notation for comments: pax <- passenger

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
# queue destinations
queueDest = [list(range(2,8,1)),list(range(8,14,1)),list(range(14,20,1)),list(range(20,26,1))]
# number of simulations
numFile = 100
WtW = [0, 25, 50, 75, 100]

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

# list of interventions
IntervList = ["FCFS", "CohortFCFS","FCFSQueueSplit"]
# compare interventions
resultCap4 = run_compareInterv(paxInfo, elevInfo, IntervList)

# WtW we are considering 
qList = [0, 25, 50, 75, 100]
# FCFS result
d0 =[ [resultCap4["Queue"][q][IntervList[0]][index][0] for index in range(numFile)] for q in qList]
# Cohorting result
d1 = [ [resultCap4["Queue"][q][IntervList[1]][index][0] for index in range(numFile)] for q in qList]
# 4 Queue Split result
d2 = [ [resultCap4["Queue"][q][IntervList[2]][index][0] for index in range(numFile)] for q in qList]


"Plot box plot"
ticks = [0, 25, 50, 75 , 100]

def set_box_color(bp, color):
    plt.setp(bp['boxes'], color=color)
    plt.setp(bp['whiskers'], color=color)
    plt.setp(bp['caps'], color=color)
    plt.setp(bp['medians'], color=color)
    
plt.figure(figsize=(6, 4))

bp2 = plt.boxplot(d1, positions=np.array(range(len(d0)))*3.0-0.2, sym='', widths=0.3)
bp7 = plt.boxplot(d2, positions=np.array(range(len(d0)))*3.0+0.2, sym='', widths=0.3)

set_box_color(bp2, "red")
set_box_color(bp7, "green")

plt.plot([], c="red", label='Cohorting')
plt.plot([], c="green", label='4 Queue Split')
plt.legend(fontsize = 16)

plt.xticks( range(0, len(ticks) * 3, 3), ticks, fontsize = 14)
plt.yticks(fontsize = 14)
plt.xlim(-1, len(ticks)*3-2)
plt.ylim(5, 20)
plt.tight_layout()

plt.xlabel("Willingness to Walk (in %)", fontsize = 16 )
plt.ylabel("Average Queue Length", fontsize = 16 )
plt.show()


