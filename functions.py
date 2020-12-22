"""
This file contains the functions used in our code. 
Notations:
pax: passenger
elev: elevator    
"""

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

#########################################################################
"""
General algebra functions
"""

"""
This function truncates a float to any number of digits

Parameters:
number: input number
digits: how many digits we want to truncate to    
output: truncated number
"""
def truncate(number, digits) -> float:
    stepper = 10.0 ** digits
    return math.trunc(stepper * number) / stepper

"""
This function element-wise adds two lists of possibly different sizes

Parmeters:
a,b: two lists
output: sum of two lists of possible different sizes
"""
def AddTwoLists(a,b):
    # if one list is smaller than the other
    if len(a) < len(b): 
        # make a copy of the larger list
        c = b.copy()
        # add smaller list element wise 
        c[:len(a)] = [sum(x) for x in zip(a,c[:len(a)])] 
    # same as previous loop, if the other list smaller than the first    
    else:
        c = a.copy()
        c[:len(b)] = [sum(x) for x in zip(b,c[:len(b)])]
    
    return(c)
"""
This function when given a large list of size k*totalNum which have a discrete
set of values listValues, creates a list of size k which contains each element
of listValues an average number of times in the large list.
For example largeList = [1,1,1,1,2,2], totalNum = 2 will give output [1,1,2].

Parameters:
largeList: input list of size k*totalNum, this could be the outputs of running
           an experiment totalNum times and collecting all the output arrays
           of size k into one large list.
totalNum:  the number of times the experiment was run
listValues: the (discrete) set of elements of the list. 
output: an array which contains "average" occurence of each element among all
        experiments- so the output array is of size k
""" 
def AverageALargeList(largeList,totalNum,listValues):
    # this counts the large list
    countValues = Counter(largeList)
    # output list
    outList = []
    for j in listValues:
        countj = countValues[j] 
        avgcountj = int(np.rint(countj/totalNum))
        # create avgcountj copies of the value j
        outList += [j]*avgcountj 
        
    return(outList)
"""
This function adds a value to the list of key values to a key. 

Parameters:
dictionary: input dictionary.
key: the key to which we want to add a value
value: the value to be added to the key    
"""      
def set_key(dictionary, key, value):
    # check if key in dictionary else add it to the dictionary
    if key not in dictionary:
        dictionary[key] = value
    # if the key already has a list of keyvalues, add the new value    
    elif type(dictionary[key]) == list:
        dictionary[key].append(value)
    else:
        dictionary[key] = [dictionary[key], value]    

#########################################################################
"""
Functions used for arrival sequence of passengers. These functions are to 
create a random arrival sequence (arrival time, destination)
"""

"""
This function generates the Poisson parameters lambda_t for each arrival.

Parameters:
t: for a particular time
T: overall time horizon
Lambda: poisson parameter    
"""
def arrPattern(t,T,Lambda):
    # generate lambda_t for non-homogenous Poisson arrival
    # current version use a constant arrival rate Lambda
    lambda_t = Lambda 
    return lambda_t

"""
This function creates an arrival file with Poisson arrivals for the passengers.
this file is used for our simulations. A certain fraction q of the arriving 
passengers are willing to walk one floor up or down from their destinations.

Parameters:
paxInfo: contains passenger configurations
Lambda: poisson parameter
T: overall time horizon
WtWList: a list of fraction of people with walking flexibility- this fraction of arriving
   passengers are willing to walk one floor up or down from their destination.
numFloor: the total number of destinations. Arriving passengers will 
          have destinations from 2 to (numFloor+1).  
numFiles: the number of random scenarios we simulate
output: a txtfile with the arrival sequence of passengers. this has four 
        columns- passenger index, arrival time (sec), destination and 
        willingness to walk one floor up or down from their destination.                
"""
def createArrivalFiles(paxInfo, numFloor, WtWList, numFiles):
    #( txtname, Lambda, T,q, numFloor):
	# q: fraction of people with walking flexibility
    # inter-arrival-time: 2750 people in 2 hours
    # T is the time horizon we simulate, 7200 sec = 2 hours
    T = 7200
    Lambda = 2750/7200
    # 
    for filename in all_files:
        arrival = [[] for i in range(len(WtWList))]
        t = 0
        k=0
        lambda_t = arrPattern(t,T,Lambda)
        time = np.random.exponential(scale = 1/lambda_t) 
        t = t+time
        # start the while loop for time
        while t<T:
            if (np.random.rand()<=lambda_t/Lambda):
                walkable = np.random.rand()
                current_time = round(t)
                level = random.choices(range(2,numFloor+2), weights=[1/(numFloor)]*(numFloor))[0]
                for i in range(len(WtWList)):
                    # w = 1 if willing to walk else 0
                    w = int(walkable <= float(WtWList[i])/100)
                    arrival[i].append([k, current_time, level, w])
                k = k+1    
            lambda_t = arrPattern(t,T,Lambda)    
            time = np.random.exponential(scale = 1/lambda_t) 
            t = t+time
        #finish the while loop for time
        for i in range(len(WtWList)):
            q = WtWList[i]
            txtname = fileName + str(q) + "%_"+str(index)+".csv"
            with open(txtname, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(arrival[i])
                
#######################################################################


"""
Functions to create dictionaries for passengers and elevators
"""

"""
This function creates a dictionary with passenger information from config file.

Parameters:
filename: passenger arrival file.
numFloor: number of floors in the building.   

Output: a dictiionary paxDict with keys ArrOrder(chronological index of
        passengers), ArrTime (arrival time from time zero of passengers),
        Dest (destination), Walk (the range of floors the passenger is willing to walk to), ServedOrNot (binary indicator
        if a passenger is served), WaitingTime (the time a passenger waited in
        the lobby from arrival to boarding), TripTime (trip time of a passenger
        once inside an elevator).
"""
def createPaxDict(filename,numFloor):
    # create the pax dictionary
    # dictionary for passenger arrivals initialized

    paxDict = pd.read_csv(filename, names=['ArrOrder','ArrTime','Dest',
                                                      'Walk']).to_dict()
    
    for somePax, walkable in paxDict['Walk'].items():
        walk = []
        if walkable:
            level = paxDict['Dest'][somePax]
            temp = [level-1, level+1]
            walk = [i for i in temp  if i>=2 and i<=(numFloor+1)]
        paxDict['Walk'][somePax] = walk
    
    # initialize other keys of the pax dictionary, they will be updated        
    paxDict['ServedOrNot']= dict.fromkeys(paxDict['ArrOrder'].keys(),False)
    # making the default waiting time to be 2 hours
    paxDict['WaitingTime']= dict.fromkeys(paxDict['ArrOrder'].keys(),7200)
    # making the default trip time to be 2 hours
    paxDict['TripTime']= dict.fromkeys(paxDict['ArrOrder'].keys(),7200)
    
    return paxDict

"""
This function creates a dictionary with elevator information from config file.

Parameters:
numElev: number of elevators in the building
elevServiceRange: the service range of all the elevators  

Output: a dictionary paxDict with keys ArrOrder(chronological index of
        passengers), ArrTime (arrival time from time zero of passengers),
        Dest (destination), Walk (WtW parameter), ServedOrNot (binary indicator
        if a passenger is served), WaitingTime (the time a passenger waited in
        the lobby from arrival to boarding), TripTime (trip time of a passenger
        once inside an elevator).
"""
def createElevDict(numElev,elevServiceRange):

    # dictionary for elevator data, output
    elevDict = {} 
    #times when elevator is at the lobby, set it to 1 in the beginning
    elevDict['NextLobby']=dict.fromkeys(range(numElev),1) 
    #any hard constraints for the elevator, e.g. floors 1-15 only
    elevDict['HardConstr'] = elevServiceRange 
    # binary- is the elevator in the lobby right now? Set it to true at the start
    elevDict['LobbyState']=dict.fromkeys(range(numElev),True) 
    #any hard constraints for the elevator, e.g. floors 1-15 only
    elevDict['SoftConstr'] = dict.fromkeys(range(numElev),[])
    
    # set soft constraints (floor ranges set by specific policies)
    # right now, all soft constraints are the hard constraints, but we could
    # set them differently
    for someElev in elevDict['HardConstr'].keys():
        elevDict['SoftConstr'][someElev] = elevDict['HardConstr'][someElev]
    
    # output
    return elevDict

"""
This function calculates the round trip time of an elevator once a group of
pasengers enter it and press their destinations

Parameters:
paxDest: list of destinations of passengers boarding an elevator
elevInfo: contains configurations of elevators in the building

Output: a number which denotes the round trip time for the elevator to come
        back to the lobby. this includes boarding and deboarding times for the 
        pax, elevator speed up and elevator speed down (with a multiplier)
"""
def RoundTripTime(paxDest,elevInfo):
    
    # total number of floors, upper bound on pax destinations
    numFloor = elevInfo[0] 
    # total number of elevators
    elevNumTotal = elevInfo[1] 
    # speed of elevator to traverse one floor
    elevSpeed = elevInfo[2]  
    # down multiplier to account for intermediate pax entering and leaving
    elevSpeedMultiplier = elevInfo[3]  
    # time to board an elevator, depends on num of pax entering
    elevBoardTime = elevInfo[4] 
    # time to deboard an elevator, depends on num of pax leaving
    elevStopTime = elevInfo[5] 
    # capacity of each elevator
    elevCap = elevInfo[7]
    
    # number of pax who have boarded in the lobby
    numPax = len(paxDest) 
    # highest floor elevator is going to go
    maxFloor = max(paxDest) 
    # count the number of pax at each destination
    countStop = [paxDest.count(i) for i in list(set(paxDest)) ] 
    
    # time to reach highest destination + total stop time
    ascentTime = (maxFloor-1)*elevSpeed + elevBoardTime[numPax-1] + sum([elevStopTime[i-1] for i in countStop])
    # time to come back to lobby. We use the multiplier here
    descentTime = (maxFloor-1)*elevSpeed*elevSpeedMultiplier
    
    #total round trip time to pick up and drop pax and back to lobby 
    # + extra door opening time in lobby, 10 secs
    roundTripTime = ascentTime + descentTime + 10
    # returns total roundtrip time
    return roundTripTime

"""
This function updates the waiting time of a passenger, once we know which
elevator they are boarding. The waiting time is the time they board the elevator
minus the time they had arrived in the building.

Parameters:
paxDict: dictionary for passenger info
boardingPax: list of passengers boarding an elevator
elevBoarded: the elev they are boarding
elevDict: dictionary for elevator info

Output: paxDict is updated with the boarding passengers being served and 
        their waiting time
"""   
def UpdatePaxWaitTime(paxDict,boardingPax,elevBoarded,elevDict):
    
    # latest time that elevator is in lobby
    elevLobbyArrTime = elevDict['NextLobby'][elevBoarded] 
    
    # for each boarding passenger, update their waiting time and status to served
    for eachPax in boardingPax:
        paxDict['WaitingTime'][eachPax] = max(0,elevLobbyArrTime - paxDict['ArrTime'][eachPax])
        paxDict['ServedOrNot'][eachPax] = True
    
    # output
    return paxDict 

"""
This function updates if an elevator is in the lobby at a given time

Parameters:
elevDict: dictionary for elev info
someElev: index of some elev whose status we want to update
currTime: current time we want to update the status of the elevator

Output: elevDict, with the 'LobbyState' of the elev being updated
"""
def IsElevatorInLobby(elevDict,someElev,currTime):
    #when is the next time elev supposed to be in the lobby
    nextTime = elevDict['NextLobby'][someElev] 
    #if current time is greater than the next time
    if currTime >= nextTime: 
        # Elev is in the lobby now
        elevDict['LobbyState'][someElev] = True 
    # output
    return elevDict    

"""
This function updates if many elevators are in the lobby at a given time

Parameters:
elevDict: dictionary for elev info
currTime: current time we want to update the status of the elevators

Output: elevDict, and we would get all the elevators in the obby at currTime
"""
def WhichElevatorsInLobby(elevDict,currTime):
    #iterate through all elevators
    for j in range(len(elevDict['NextLobby'].keys())):
        # Use function for each elevator
        elevDict = IsElevatorInLobby(elevDict,j,currTime) 
    # this output should have all elevators in lobby    
    return elevDict 

"""
This function checks if there are any unserved pax waiting in line at a given time

Parameters:
paxDict: dictionary for passenger info
currTime: current time we want to check the status of pax
queueSplit: are we checking this under the QueueSplit intervention
queueDestRange: range of destinations for diff queues under the QueueSplit intervention

Output: list of unserved pax in the line at current time
"""
def UnservedPaxinQueue(paxDict,currTime,queueSplit=False,queueDestRange=[]):
    #if we are not splitting queues in the lobby
    if queueSplit == False:
        # who arrived so far
        paxSoFar = [j for j in paxDict['ArrTime'].keys() if paxDict['ArrTime'][j] <= currTime]
    #if there is a queue Split,
    else: 
        # who arrived so far and whose dest are in queueDestRange
        paxSoFar = [j for j in paxDict['ArrTime'].keys() if (paxDict['ArrTime'][j] <= currTime) and (paxDict['Dest'][j] in queueDestRange)]
    
    # among those who arrived, who are unserved
    unservedPax = [j for j in paxSoFar if paxDict['ServedOrNot'][j] == False]  
    # output the list of pax not yet served
    return unservedPax

"""
This function. given a pax and an elev returns if that pax can take that elev

Parameters:
paxDict: dictionary for passenger info
somePax: a given passenger
someElevDestList: list of destionations a given elev can serve
"""
def CanPaxTakeThisElevator(paxDict,somePax,someElevDestList):
    # all possible destinations this pax can go to, including WtW parameter
    thisPaxDest = [paxDict['Dest'][somePax]] + paxDict['Walk'][somePax]
    #can pax board this elev
    return bool(any(list(set(thisPaxDest) & set(someElevDestList)))) 

"""
This function outputs the trip time of each pax, when given a list of pax 
who enter an elev in the lobby and press their destinations(s)
Parameters:
paxList: list of pax who enter an elev
paxDest: list of destinations of the boarding pax
elevInfo: contains configurations of elevators in the building

Output: a list of trip times for each pax in the elevator, this is simply
        how much time they spend in the elevator
"""
def PaxTripTime(paxList,paxDest,elevInfo):

    # total number of floors, upper bound on pax destinations
    numFloor = elevInfo[0] 
    # total number of elevators
    elevNumTotal = elevInfo[1] 
    # speed of elevator to traverse one floor
    elevSpeed = elevInfo[2]  
    # down multiplier to account for intermediate pax entering and leaving
    elevSpeedMultiplier = elevInfo[3]  
    # time to board an elevator, depends on num of pax entering
    elevBoardTime = elevInfo[4] 
    # time to deboard an elevator, depends on num of pax leaving
    elevStopTime = elevInfo[5] 
    # capacity of each elevator
    elevCap = elevInfo[7]
    
    # number of pax who have boarded in the lobby
    numPax = len(paxList) 
    # highest floor elevator is going to go
    maxFloor = max(paxDest) 
    # count the number of pax at each destination
    countStop = [paxDest.count(i) for i in list(set(paxDest)) ] 
    # sort passenger destinations by index
    sortedDest = np.argsort(paxDest)

    # Only counts time to ascend to the destination of each pax   
    ascentTime = [(j-1)*elevSpeed + elevBoardTime[numPax-1] for j in paxDest]
    # time to reach highest destination + total stop time
    tripTime = []
    #stores cumulative stopping times
    stopTime = [0]*numPax 
    counter = 0

    for i in countStop:
        # counts stopping time at each stop, depends on number of pax deboarding
        currStopTime = elevStopTime[i-1]
        for j in range(counter,numPax):
            # adds up stop times in earlier stop to later stop
            stopTime[sortedDest[j]] += currStopTime
        counter += i

    tripTime = [a + b for a, b in zip(ascentTime,stopTime)] 
    # returns total roundtrip time
    return tripTime 
    
"""
This function returns a list of pax in line who can cohort to a given target 
floor, knowing the remaining capacity of an elev.

Parameters:
paxDict: dictionary for passenger info
lobbyQueue: current queue in the lobby
targetFloor: the floor to which we want to cohort other pax to
remElevCap: remaining capacity of the elevator

Output: list of pax who can go to targetFloor, respecting remaining capacity
        of the elevator
"""
def CohortInQueue(paxDict,lobbyQueue,targetFloor,remElevCap):
    # variable to index through the queue
    j = 1 
    # find the other pax to join the cohort
    cohortFollowers = [] 
    # while we are still parsing lobbyQueue and elevator is unfilled
    while (j < len(lobbyQueue) and len(cohortFollowers)<remElevCap-1):
        # dest for current person in queue, including WtW
        currDest = [paxDict['Dest'][lobbyQueue[j]]] + paxDict['Walk'][j] 

        # if any pax can reach the target floor
        if (targetFloor in currDest): 
            # add to list of cohort followers
            cohortFollowers.append(lobbyQueue[j])
        j+=1     
    # outputs in FCFS order, enough followers to cohort to targetfloor    
    return cohortFollowers 

"""
This function takes first N people in a queue, given N. If there are less than
N people in a queue, select everyone. (used in queue splitting)

Parameters:
someQueue: a given queue
N: number of people we want to pick

Output: return the first N people (or everyone if there are less than N)
"""
def FirstNpax(someQueue,N):
    if len(someQueue) > N:
        someQueue = someQueue[0:N]
    return(someQueue) 

"""
This function in realtime, allocates pax to next possible queue if pax is willing to walk

Parameters:
paxDict: dictionary of pax info
currTime: current time we want to allocate the pax
currQueue: current queue that we are working on, among the many in queue splitting intervention
queueDestRange: range of destinations for diff queues under the QueueSplit intervention

Output: 
"""
def AllocateUnservedPaxToQueue(paxDict,currTime,currQueue,queueDestRange): 
    # list of passengers who have arrived and not yet served
    paxList = [j for j in paxDict['ArrTime'].keys() if (paxDict['ArrTime'][j] <= currTime) and (paxDict['ServedOrNot'][j] == False)]
    # among everyone in paxList, who is not yet allocated
    unallocatedPax = [j for j in paxList if j not in list([ item for key in range(len(currQueue)) for item in currQueue[key]])]
    # for each pax unallocated,
    for somePax in unallocatedPax:
        # range of destinations (with WtW) the pax can go to
        thisPaxDest = [paxDict['Dest'][somePax]] + paxDict['Walk'][somePax]
        potentialQueue = [len(currQueue[i])  if bool(any(list(set(queueDestRange[i]) & set(thisPaxDest)))) else 5000 for i in range(len(queueDestRange)) ]
        queueIndex = np.argmin(potentialQueue)
        currQueue[queueIndex] =list(currQueue[queueIndex]+[somePax])
    return currQueue

#######################################################################
"""
Functions that are implement the interventions we propose
"""

"""
This function implements any elevator intervention given soft constraints on
the elevator (e.g. FCFS, allocate odd or even etc.)

Parameters:
elevDict: dictionary of elev info
paxDict: dictionary of pax info
elevInfo: contains configurations of elevators in the building

Output: an implementation of the intervention, with the following outputs:
Waiting time of all pax, queue size over time, list of loads of elevators,
list of trip times of all pax, number of stops on each elevator trip    
"""
def ElevIntervSoftConstr(elevDict,paxDict,elevInfo):

    # total number of floors, upper bound on pax destinations
    numFloor = elevInfo[0] 
    # total number of elevators
    elevNumTotal = elevInfo[1] 
    # speed of elevator to traverse one floor
    elevSpeed = elevInfo[2]  
    # down multiplier to account for intermediate pax entering and leaving
    elevSpeedMultiplier = elevInfo[3]  
    # time to board an elevator, depends on num of pax entering
    elevBoardTime = elevInfo[4] 
    # time to deboard an elevator, depends on num of pax leaving
    elevStopTime = elevInfo[5] 
    # capacity of each elevator
    elevCap = elevInfo[7]    
    
    #Current Time
    currTime = 0
    # size of the queue at each timestep
    queueSize = []
    # load of each elevator trip
    loadSize = []
    # number of buttons pressed= number of stops made in each elevator trip
    buttonPress = []
    # Are there unserved pax overall and time does not exceed twice the rush hour window
    while(False in paxDict['ServedOrNot'].values()) and (currTime < 14400): 
        # move to the next time, we increment in steps of 10s.
        currTime += 10 
        # given current time, update elevDict
        elevDict = WhichElevatorsInLobby(elevDict,currTime)
        # create an array of pax indices who have arrived to form a queue
        lobbyQueue = UnservedPaxinQueue(paxDict,currTime)
        # store the size of the queue at the current time
        queueSize.append(len(lobbyQueue))
        # Are there empty elevators in the lobby and unserved pax in the queue
        if(any(elevDict['LobbyState'].values()) and len(lobbyQueue)>0):
            # list of available elev
            availableElev = [j for j in elevDict['LobbyState'].keys() if elevDict['LobbyState'][j] == True]
            # initialize a list of pax who board the elevators
            elevPax = dict.fromkeys(availableElev,[]) 
            # initialize a list of the destinations of pax who board the elevators
            elevPaxDest =  dict.fromkeys(availableElev,[])
            # this will iterate over waiting pax in the line, this is an index for unserved pax.
            indexPax = 0 
        
            # while there are available elevators and we haven't yet served all pax
            while (len(availableElev)>0) and (indexPax<len(lobbyQueue)):
                # pax at the head of the line
                somePax = lobbyQueue[indexPax]
                # list of destinations they can go to, including WtW
                paxDestList = [paxDict['Dest'][somePax]] + paxDict['Walk'][somePax]
                
                # index of destinations being considered for somePax
                indexDest = 0
                signal = 0 # signal (indicator) of this pax being served
                # while we consider this destination and the pax hasn't been served
                while (indexDest < len(paxDestList)) and (not signal):
                    
                    # search through the Destination of this pax and check whether there is an elevator that serves
                    feasibleElev = [j for j in availableElev if paxDestList[indexDest] in elevDict['SoftConstr'][j]]
                    if not any(feasibleElev):
                        # no feasible elevator directly to the destination
                        indexDest+=1
                    else:
                        # we have some elevator go to the destination
                        # send the pax into feasibleElev[0]
                        signal = 1 # this pax is served
                        elevIndex = feasibleElev[0]

                        # add this pax to the list of pax being served by this elev
                        elevPax[ elevIndex ] = elevPax[ elevIndex ] +[somePax]
                        # add destination of this pax
                        elevPaxDest[ elevIndex ] = elevPaxDest[elevIndex] + [paxDestList[indexDest]]
                        # have we filled the elevator
                        if len(elevPax[elevIndex])==elevCap:
                            # elevator is full, so it could leave the lobby
                            elevDict['LobbyState'][elevIndex] = False
                            # update waiting time of the pax
                            paxDict = UpdatePaxWaitTime(paxDict,elevPax[elevIndex],elevIndex,elevDict)
                            # calculate trip times of the pax
                            tripTimes = PaxTripTime(elevPax[elevIndex],elevPaxDest[elevIndex],elevInfo)
                            
                            # update trip times of pax
                            for j in range(len(elevPax[elevIndex])): 
                                paxDict['TripTime'][elevPax[elevIndex][j]] = tripTimes[j]
                            # update number of button presses (stops) made in this elevator
                            buttonPress += [len(set(elevPaxDest[elevIndex]))]
                            # calculate round trip time of this elev
                            roundTripTime = RoundTripTime(elevPaxDest[elevIndex],elevInfo)
                            # update next time this elev returns to the lobby
                            elevDict['NextLobby'][elevIndex] = currTime + roundTripTime 
                            # this elev is removed from list of available elev
                            availableElev.remove(elevIndex)
                            # update list of loads 
                            loadSize.append(elevCap)
                indexPax +=1
                
            # list of elevs that depart even if they are not full
            departList = [j for j in availableElev if any(elevPax[j])]
            # for some elev in this list
            for someElev in departList:
                # elev leaves the lobby
                elevDict['LobbyState'][someElev] = False
                # update waiting time of the pax
                paxDict = UpdatePaxWaitTime(paxDict,elevPax[someElev],someElev,elevDict)
                # update trip times of pax
                tripTimes = PaxTripTime(elevPax[someElev],elevPaxDest[someElev],elevInfo)
                # update trip times of pax
                for j in range(len(elevPax[someElev])): 
                    paxDict['TripTime'][elevPax[someElev][j]] = tripTimes[j]
                # update number of button presses (stops) made in this elevator
                buttonPress += [len(set(elevPaxDest[someElev]))]
                # calculate round trip time of this elev
                roundTripTime = RoundTripTime(elevPaxDest[someElev],elevInfo)
                # update next time this elev returns to the lobby
                elevDict['NextLobby'][someElev] = currTime + roundTripTime 
                # this elev is removed from list of available elev
                availableElev.remove(someElev)
                # update list of loads 
                loadSize.append(len(elevPax[someElev]))
    # output
    return (list(paxDict['WaitingTime'].values()), queueSize, loadSize, list(paxDict['TripTime'].values()),buttonPress)     
    
"""
This function implements the cohorting intervention.

Parameters:
elevDict: dictionary of elev info
paxDict: dictionary of pax info
elevInfo: contains configurations of elevators in the building

Output: an implementation of the intervention, with the following outputs:
Waiting time of all pax, queue size over time, list of loads of elevators,
list of trip times of all pax, number of stops on each elevator trip    
"""
def ElevIntervCohorting(elevDict,paxDict,elevInfo):   
 
    # total number of floors, upper bound on pax destinations
    numFloor = elevInfo[0] 
    # total number of elevators
    elevNumTotal = elevInfo[1] 
    # speed of elevator to traverse one floor
    elevSpeed = elevInfo[2]  
    # down multiplier to account for intermediate pax entering and leaving
    elevSpeedMultiplier = elevInfo[3]  
    # time to board an elevator, depends on num of pax entering
    elevBoardTime = elevInfo[4] 
    # time to deboard an elevator, depends on num of pax leaving
    elevStopTime = elevInfo[5] 
    # capacity of each elevator
    elevCap = elevInfo[7]    
    
    #Current Time
    currTime = 0
    # size of the queue at each timestep
    queueSize = []
    # load of each elevator trip
    loadSize = []
    # number of buttons pressed= number of stops made in each elevator trip
    buttonPress = []
    # Are there unserved pax overall and time does not exceed twice the rush hour window
    while(False in paxDict['ServedOrNot'].values() and (currTime < 14400)): 
        # move to the next time, we increment in steps of 10s.
        currTime += 10 
        # given current time, update elevDict
        elevDict = WhichElevatorsInLobby(elevDict,currTime)
        # create an array of pax indices who have arrived to form a queue
        lobbyQueue = UnservedPaxinQueue(paxDict,currTime)
        # store the size of the queue at the current time
        queueSize.append(len(lobbyQueue))
        # Are there empty elevators in the lobby and unserved pax in the queue
        if(any(elevDict['LobbyState'].values()) and len(lobbyQueue)>0):
            # list of available elev
            availableElev = [j for j in elevDict['LobbyState'].keys() if elevDict['LobbyState'][j] == True]
            # this will iterate over waiting pax in the line, this is an index for unserved pax.
            indexPax = 0 
            
            # while there are available elevators and we haven't yet served all pax
            while (len(availableElev)>0 and indexPax<len(lobbyQueue)):
                # leader/pax at head of the line, to cohort
                cohortLeader = lobbyQueue[indexPax] 
                # list of destinations they can go to, including WtW
                cohortDestList = [paxDict['Dest'][cohortLeader]] + paxDict['Walk'][cohortLeader]
                
                # search through the Destination of this pax and check whether there is an elevator can serve
                feasibleElev = []
                # index of destinations being considered for somePax
                indexDest= 0
                # while we consider this destination and if no feasible elev
                while indexDest<len(cohortDestList) and not any(feasibleElev):
                    # list of feasible elevators
                    feasibleElev = [j for j in availableElev if cohortDestList[indexDest] in elevDict['SoftConstr'][j]]
                    # move to the next dest
                    indexDest +=1
                # no feasible elevator directly to the destination
                if not any(feasibleElev):
                    # move to the next pax
                    indexPax+=1
                # have some elevator go to the destination
                else:
                    # pick the first feasible elev
                    elevIndex = feasibleElev[0]
                    # list of dest this elev can serve
                    thisElevDestList = elevDict['SoftConstr'][elevIndex]
                    # targetFloor is the stop that cohortLeader will go to
                    targetFloor = cohortDestList[indexDest-1]  
                    # find other possible pax to cohort with
                    cohortFollowers = CohortInQueue(paxDict,lobbyQueue[indexPax:],targetFloor,elevCap)
                    #list of all boarding pax for this elev.
                    cohortFollowers.append(cohortLeader) 
                    # List of all destinations of this cohort
                    cohortDestList =[ targetFloor]*len(cohortFollowers)
                    # current load of the elevator is all the pax in this cohort
                    currElevLoad = len(cohortFollowers)
                    # consider remaining pax in the queue
                    lobbyQueue2 =  [j for j in lobbyQueue if j not in cohortFollowers]
                    # make sure we only check pax who can board this elevator
                    lobbyQueue2 = [j for j in lobbyQueue2 if CanPaxTakeThisElevator(paxDict,j,thisElevDestList)] 
                    
                    # while the elev is not filled and there are some pax to consider
                    while (currElevLoad < elevCap) and (len(lobbyQueue2)>0):
                        # leader/pax at head of the line, to cohort
                        cohortLeader2 = lobbyQueue2[0]
                        # list of destinations they can go to, including WtW
                        cohortDestList2 = [paxDict['Dest'][cohortLeader2]] + paxDict['Walk'][cohortLeader2]
                        #  targetFloor2 is the stop that cohortLeader2 will go to
                        targetFloor2 =  next((a for a in cohortDestList2 if a in set(thisElevDestList)), None)
                        # find other possible pax to cohort with
                        cohortFollowers2 = CohortInQueue(paxDict,lobbyQueue2,targetFloor2,elevCap-currElevLoad)
                        #list of pax boarding this elev in *this* cohort
                        cohortFollowers2.append(cohortLeader2)
                        # List of all destinations of this cohort
                        cohortDestList += [targetFloor2]*len(cohortFollowers2)
                        # list of all pax boarding this elevator
                        cohortFollowers += cohortFollowers2
                        # current load of the elevator
                        currElevLoad += len(cohortFollowers2)
                        # update the lobby queue
                        lobbyQueue2 = [j for j in lobbyQueue2 if j not in cohortFollowers]
                    # update waiting time of the pax   
                    paxDict = UpdatePaxWaitTime(paxDict,cohortFollowers,elevIndex,elevDict)
                    # elevator is full, so it could leave the lobby                      
                    elevDict['LobbyState'][elevIndex] = False
                    # calculate round trip time of this elev
                    roundTripTime = RoundTripTime(cohortDestList,elevInfo)
                    # update next time this elev returns to the lobby
                    elevDict['NextLobby'][elevIndex] = currTime + roundTripTime 
                    # this elev is removed from list of available elev
                    availableElev.remove(elevIndex)
                    # update number of button presses (stops) made in this elevator
                    buttonPress += [len(set(cohortDestList))]
                    # update list of loads 
                    loadSize.append(len(cohortFollowers))
                    # calculate trip times of the pax
                    tripTimes = PaxTripTime(cohortFollowers,cohortDestList,elevInfo)
                    # update trip times of pax
                    for j in range(len(cohortFollowers)): 
                        paxDict['TripTime'][cohortFollowers[j]] = tripTimes[j]
                    
                    # update the lobby queue to those who haven't been served
                    lobbyQueue = [j for j in lobbyQueue if paxDict['ServedOrNot'][j] == False]
            

    return (list(paxDict['WaitingTime'].values()), queueSize, loadSize, list(paxDict['TripTime'].values()),buttonPress)            
 
"""
This function implements the queue splitting intervention.

Parameters:
elevDict: dictionary of elev info
paxDict: dictionary of pax info
elevInfo: contains configurations of elevators in the building
paxInfo: contains passenger configurations

Output: an implementation of the intervention, with the following outputs:
Waiting time of all pax, queue size over time, list of loads of elevators,
list of trip times of all pax, number of stops on each elevator trip, as well
as the sizes of each queue over time  
"""
def ElevIntervQueueSplit(elevDict,paxDict,elevInfo,paxInfo):

    # total number of floors, upper bound on pax destinations
    numFloor = elevInfo[0] 
    # total number of elevators
    elevNumTotal = elevInfo[1] 
    # speed of elevator to traverse one floor
    elevSpeed = elevInfo[2]  
    # down multiplier to account for intermediate pax entering and leaving
    elevSpeedMultiplier = elevInfo[3]  
    # time to board an elevator, depends on num of pax entering
    elevBoardTime = elevInfo[4] 
    # time to deboard an elevator, depends on num of pax leaving
    elevStopTime = elevInfo[5] 
    # capacity of each elevator
    elevCap = elevInfo[7]     

    # the floor ranges for all queues 
    queueDest = paxInfo[2]
    # number of queue splits
    numQueues = len(paxInfo[2])

    #Current Time
    currTime = 0
    # size of the queue at each timestep
    queueSize = []
    # load of each elevator trip
    loadSize = []
    # number of buttons pressed= number of stops made in each elevator trip
    buttonPress = []
    # we want to track size of each queue, over time 
    eachQueueSize = {k: [] for k in range(numQueues)} 
    # create dict with one key for each queue
    lobbyQueue = {k: [] for k in range(numQueues)} 
    
    # which queue are we looking at right now
    whichQueue = 0
    # Are there unserved pax overall and time does not exceed twice the rush hour window
    while (False in paxDict['ServedOrNot'].values()) and (currTime < 14400): 
        # move to the next time, we increment in steps of 10s.
        currTime += 10 
        # given current time, update elevDict
        elevDict = WhichElevatorsInLobby(elevDict,currTime)
        # for each queue
        for eachQueue in range(numQueues):
            # write out the range of floors
            eachQueueDest = queueDest[eachQueue]
                    
            # the pax in this queue
            lobbyQueue[eachQueue] = UnservedPaxinQueue(paxDict,currTime,True,eachQueueDest)
            # track size of each of the queues over time    
            set_key(eachQueueSize, eachQueue, len(lobbyQueue[eachQueue])) 
        #tracking the size of the total number of pax in the lobby
        queueSize.append(sum(eachQueueSize[j][-1] for j in eachQueueSize.keys())) 
        
        # length of overall lobby queue
        lenLobbyQueue = queueSize[-1]
        # Are there empty elevators in the lobby and unserved pax in the queue
        if (any(elevDict['LobbyState'].values()) and lenLobbyQueue>0): 
            # list of available elev
            availableElev = [j for j in elevDict['LobbyState'].keys() if elevDict['LobbyState'][j] == True]
            # initialize a list of pax who board the elevators
            elevPax = dict.fromkeys(availableElev,[]) 
            # initialize a list of the destinations of pax who board the elevators
            elevPaxDest =  dict.fromkeys(availableElev,[])
            # this will iterate over waiting pax in the line, this is an index for unserved pax.
            indexTotalLobbyQueue = 0
            # how many times are we cycling through each queue
            cycling = 0 

            # while there are available elevators and we haven't cycled
            # through all the queues without any action
            while (len(availableElev)>0) and (cycling < numQueues): 
                # if the current queue is empty
                if (not any(lobbyQueue[whichQueue])): 
                    # Move to next queue
                    whichQueue = (whichQueue+ 1)%numQueues 
                    # cycle once more
                    cycling += 1
                else:
                    # Take the group of pax at head of whichQueue
                    someGroupPax = FirstNpax(lobbyQueue[whichQueue],elevCap).copy() 
                    # first pax in this group
                    groupLeader = someGroupPax[0] 
                    # dest of groupLeader
                    groupLeaderDest = paxDict['Dest'][groupLeader] 
                    # find a feasible elevator
                    feasibleElev = [j for j in availableElev if groupLeaderDest in elevDict['SoftConstr'][j]] 
                
                     # if no feasible elev, move to next queue
                    if not any(feasibleElev):
                        # cycle once more
                        cycling += 1
                    else:
                        # pick first feasible elevator
                        elevIndex = feasibleElev[0]
                        # reset cycling to 0 since we are going to load an elev
                        cycling = 0
                        # these pax will board this elevator
                        elevPax[ elevIndex ] = someGroupPax.copy() 
                        # add destination of these pax
                        elevPaxDest[ elevIndex ] = [paxDict['Dest'][j] for j in someGroupPax] 
                        # current load of this elevator
                        currLoad = len(someGroupPax)
                        for j in range(0,currLoad,1):
                            # Remove this group of pax from whichQueue
                            del lobbyQueue[whichQueue][0] 
                        
                        # another cycling variable to fill up remaining elev capacity
                        cycling2=0
                        # while this elev is not yet full and we haven't cycled
                        # through all the queues without any action
                        while (currLoad<elevCap) and (cycling2<numQueues):
                            # move to next queue
                            whichQueue = (whichQueue+ 1)%numQueues 
                            # if the current queue is not empty
                            if any(lobbyQueue[whichQueue]):
                                # Take the group of pax at head of whichQueue
                                remGroupPax = FirstNpax(lobbyQueue[whichQueue],elevCap-currLoad).copy()
                                # first pax in this group
                                remGroupLeader = remGroupPax[0] 
                                # dest of groupLeader
                                remGroupLeaderDest = paxDict['Dest'][remGroupLeader] 
                                # if this destination is served by the elevator
                                if remGroupLeaderDest in elevDict['SoftConstr'][elevIndex]:
                                     # This group will also board this elevator
                                    elevPax[ elevIndex ] += remGroupPax.copy() 
                                     # adding their destinations
                                    elevPaxDest[ elevIndex ] += [paxDict['Dest'][j] for j in remGroupPax] 
                                     # update load of this elevator
                                    currLoad += len(remGroupPax)
                                    for j in range(0,len(remGroupPax),1):
                                         # Remove this group of pax from whichQueue
                                        del lobbyQueue[whichQueue][0] 
                            # cycle once more             
                            cycling2 += 1       
                         
                        # elevator is full, so it could leave the lobby
                        elevDict['LobbyState'][elevIndex] = False
                        # update waiting time of the pax
                        paxDict = UpdatePaxWaitTime(paxDict,elevPax[elevIndex],elevIndex,elevDict)
                        # calculate trip times of the pax
                        tripTimes = PaxTripTime(elevPax[elevIndex],elevPaxDest[elevIndex],elevInfo)
                         # these many pax in current lobby have been served
                        indexTotalLobbyQueue += len(elevPax[elevIndex])
                        
                        # Update trip times of pax
                        for j in range(len(elevPax[elevIndex])): 
                            paxDict['TripTime'][elevPax[elevIndex][j]] = tripTimes[j]
                        # update number of button presses (stops) made in this elevator
                        buttonPress += [len(set(elevPaxDest[elevIndex]))]
                        # calculate round trip time of this elev
                        roundTripTime = RoundTripTime(elevPaxDest[elevIndex],elevInfo)
                        # update next time this elev returns to the lobby
                        elevDict['NextLobby'][elevIndex] = currTime + roundTripTime #update next lobby time for that eleavtor
                        # this elev is removed from list of available elev
                        availableElev.remove(elevIndex)
                        # update list of loads 
                        loadSize.append(elevCap)
                    # move to next queue
                    whichQueue = (whichQueue+ 1)%numQueues 
 
    return (list(paxDict['WaitingTime'].values()),queueSize, loadSize, list(paxDict['TripTime'].values()),buttonPress,eachQueueSize)     
 

"""
This function implements the cohorting intervention in limited lobby space

Parameters:
elevDict: dictionary of elev info
paxDict: dictionary of pax info
elevInfo: contains configurations of elevators in the building
lobbySize: the number of people that Queue Manager can access
cohortSize: the number of people that Queue Manager tries to group together

Output: an implementation of the intervention, with the following outputs:
Waiting time of all pax, queue size over time, list of loads of elevators,
list of trip times of all pax, number of stops on each elevator trip    
"""
def ElevIntervLimitedCohorting(elevDict,paxDict,elevInfo,lobbySize,cohortSize):   

    # total number of floors, upper bound on pax destinations
    numFloor = elevInfo[0] 
    # total number of elevators
    elevNumTotal = elevInfo[1] 
    # speed of elevator to traverse one floor
    elevSpeed = elevInfo[2]  
    # down multiplier to account for intermediate pax entering and leaving
    elevSpeedMultiplier = elevInfo[3]  
    # time to board an elevator, depends on num of pax entering
    elevBoardTime = elevInfo[4] 
    # time to deboard an elevator, depends on num of pax leaving
    elevStopTime = elevInfo[5] 
    # capacity of each elevator
    elevCap = elevInfo[7] 
    
    #Current Time
    currTime = 0
    # size of the queue at each timestep
    queueSize = []
    # load of each elevator trip
    loadSize = []
    # number of buttons pressed= number of stops made in each elevator trip
    buttonPress = []
    # Are there unserved pax overall and time does not exceed twice the rush hour window
    while(False in paxDict['ServedOrNot'].values() and (currTime < 14400)): 
        # move to the next time, we increment in steps of 10s.
        currTime += 10 
        # given current time, update elevDict
        elevDict = WhichElevatorsInLobby(elevDict,currTime)
        # create an array of pax indices who have arrived to form a queue
        lobbyQueue = UnservedPaxinQueue(paxDict,currTime)
        # store the size of the queue at the current time
        queueSize.append(len(lobbyQueue))
        # Are there empty elevators in the lobby and unserved pax in the queue
        if(any(elevDict['LobbyState'].values()) and len(lobbyQueue)>0):
            # list of available elev
            availableElev = [j for j in elevDict['LobbyState'].keys() if elevDict['LobbyState'][j] == True]
            # this will iterate over waiting pax in the line, this is an index for unserved pax.
            indexPax = 0             
            # while there are available elevators and we haven't yet served all pax
            while (len(availableElev)>0 and indexPax<len(lobbyQueue)):
                # leader/pax at head of the line, to cohort
                cohortLeader = lobbyQueue[indexPax] 
                # list of destinations they can go to, including WtW
                cohortDestList = [paxDict['Dest'][cohortLeader]] + paxDict['Walk'][cohortLeader]
                
                # search through the Destination of this pax and check whether there is an elevator can serve
                feasibleElev = []
                # index of destinations being considered for somePax
                indexDest= 0
                # while we consider this destination and if no feasible elev
                while indexDest<len(cohortDestList) and not any(feasibleElev):
                    # list of feasible elevators
                    feasibleElev = [j for j in availableElev if cohortDestList[indexDest] in elevDict['SoftConstr'][j]]
                    # move to the next dest
                    indexDest +=1
                # no feasible elevator directly to the destination
                if not any(feasibleElev):
                    # move to the next pax
                    indexPax+=1
                # have some elevator go to the destination
                else:
                    # pick the first feasible elev
                    elevIndex = feasibleElev[0]
                    # list of dest this elev can serve
                    thisElevDestList = elevDict['SoftConstr'][elevIndex]
                    # targetFloor is the stop that cohortLeader will go to
                    targetFloor = cohortDestList[indexDest-1]  
                    # the lobby pax QM can potentially ask
                    askList = lobbyQueue[indexPax:indexPax+lobbySize]
                    # find other possible pax to cohort with
                    cohortFollowers = CohortInQueue(paxDict,askList,targetFloor,cohortSize)
                    #list of all boarding pax for this elev
                    cohortFollowers.append(cohortLeader) 
                    # List of all destinations of this cohort
                    cohortDestList =[targetFloor]*len(cohortFollowers)
                    # current load of the elevator is all the pax in this cohort
                    currElevLoad = len(cohortFollowers)
                    # consider remaining pax in the queue
                    tempQueue = [ pax for pax in lobbyQueue if pax not in cohortFollowers]
                    # consider remaining pax in the queue
                    lobbyQueue2 = [ pax for pax in lobbyQueue if pax not in cohortFollowers]
                    # make sure we only check pax who can board this elevator
                    lobbyQueue2 = [j for j in lobbyQueue2 if CanPaxTakeThisElevator(paxDict,j,thisElevDestList)] 
                    # while the elev is not filled and there are some pax to consider
                    while (currElevLoad < elevCap) and (len(lobbyQueue2)>0):
                        # leader/pax at head of the line, to cohort
                        cohortLeader2 = lobbyQueue2[0]
                        # index pax for remaining
                        indexPax2 = tempQueue.index(cohortLeader2)
                        # list of destinations they can go to, including WtW
                        cohortDestList2 = [paxDict['Dest'][cohortLeader2]] + paxDict['Walk'][cohortLeader2]
                        #  targetFloor2 is the stop that cohortLeader2 will go to
                        targetFloor2 =  next((a for a in cohortDestList2 if a in set(thisElevDestList)), None)
                        # if only one spot is left, just ask cohortLeader2 to board
                        if elevCap-currElevLoad==1:
                            cohortFollowers2 = []
                        # else find more pax to cohort with cohortLeader2
                        else:
                            # list of pax the QM can talk to
                            askList = tempQueue[indexPax2:indexPax2+lobbySize]
                            # find other possible pax to cohort with
                            cohortFollowers2 = CohortInQueue(paxDict,askList,targetFloor2,
                                                             min(cohortSize, elevCap-currElevLoad))
                        # list of pax boarding this elev in *this* cohort
                        cohortFollowers2.append(cohortLeader2) 
                        # List of all destinations of this cohort
                        cohortDestList += [targetFloor2]*len(cohortFollowers2)
                        # list of all pax boarding this elevator
                        cohortFollowers += cohortFollowers2
                        # current load of the elevator
                        currElevLoad += len(cohortFollowers2)
                        # update the lobby queue
                        lobbyQueue2 =  [ pax for pax in lobbyQueue2 if pax not in cohortFollowers]
                        # update the tempQueue
                        tempQueue = [j for j in tempQueue if j not in cohortFollowers]
                    # update waiting time of the pax  
                    paxDict = UpdatePaxWaitTime(paxDict,cohortFollowers,elevIndex,elevDict)
                    # elevator is full, so it could leave the lobby                        
                    elevDict['LobbyState'][elevIndex] = False
                    # calculate round trip time of this elev
                    roundTripTime = RoundTripTime(cohortDestList,elevInfo)
                    # update next time this elev returns to the lobby
                    elevDict['NextLobby'][elevIndex] = currTime + roundTripTime #update next lobby time for that eleavtor
                    # this elev is removed from list of available elev
                    availableElev.remove(elevIndex)
                    # update number of button presses (stops) made in this elevator
                    buttonPress += [len(set(cohortDestList))]
                    # update list of loads 
                    loadSize.append(len(cohortFollowers))
                    # calculate trip times of the pax
                    tripTimes = PaxTripTime(cohortFollowers,cohortDestList,elevInfo)
                    # Update trip times of pax
                    for j in range(len(cohortFollowers)): 
                        paxDict['TripTime'][cohortFollowers[j]] = tripTimes[j]
                    # update the lobby queue to those who haven't been served
                    lobbyQueue = [j for j in lobbyQueue if paxDict['ServedOrNot'][j] == False]
            

    return (list(paxDict['WaitingTime'].values()), queueSize, loadSize, list(paxDict['TripTime'].values()),buttonPress)            

"""
This function implements the Queue Split intervention with passengers willing to walk
Parameters:
elevDict: dictionary of elev info
paxDict: dictionary of pax info
elevInfo: contains configurations of elevators in the building
paxInfo: contains passenger configurations

Output: an implementation of the intervention, with the following outputs:
Waiting time of all pax, queue size over time, list of loads of elevators,
list of trip times of all pax, number of stops on each elevator trip  
"""
# "Intervention: SoftConstraints with Queue Split and round robin among queues for pax to get in"
# passenger will choose the shorter queue to join when arrive
def ElevIntervQueueSplitwithWalking(elevDict,paxDict,elevInfo,paxInfo):

    # total number of floors, upper bound on pax destinations
    numFloor = elevInfo[0] 
    # total number of elevators
    elevNumTotal = elevInfo[1] 
    # speed of elevator to traverse one floor
    elevSpeed = elevInfo[2]  
    # down multiplier to account for intermediate pax entering and leaving
    elevSpeedMultiplier = elevInfo[3]  
    # time to board an elevator, depends on num of pax entering
    elevBoardTime = elevInfo[4] 
    # time to deboard an elevator, depends on num of pax leaving
    elevStopTime = elevInfo[5] 
    # capacity of each elevator
    elevCap = elevInfo[7]     

    # the floor ranges for all queues 
    queueDest = paxInfo[2]
    # number of queue splits
    numQueues = len(paxInfo[2])

    #Current Time
    currTime = 0
    # size of the queue at each timestep
    queueSize = []
    # load of each elevator trip
    loadSize = []
    # number of buttons pressed= number of stops made in each elevator trip
    buttonPress = []
    # we want to track size of each queue, over time 
    eachQueueSize = {k: [] for k in range(numQueues)} 
    # create dict with one key for each queue
    lobbyQueue = {k: [] for k in range(numQueues)} 
    
    # which queue are we looking at right now
    whichQueue = 0
    # Are there unserved pax overall and time does not exceed twice the rush hour window
    while (False in paxDict['ServedOrNot'].values()) and (currTime < 14400): 
        # move to the next time, we increment in steps of 10s.
        currTime += 10 
        # given current time, update elevDict
        elevDict = WhichElevatorsInLobby(elevDict,currTime)
        # for each queue
        lobbyQueue = AllocateUnservedPaxToQueue(paxDict,currTime,lobbyQueue, queueDest)
        
        for eachQueue in range(numQueues):
            # write out the range of floors
            eachQueueDest = queueDest[eachQueue]
                    
            # the pax in this queue
#             lobbyQueue[eachQueue] = UnservedPaxinQueue(paxDict,currTime,True,eachQueueDest)
            # track size of each of the queues over time    
            set_key(eachQueueSize, eachQueue, len(lobbyQueue[eachQueue])) 
        #tracking the size of the total number of pax in the lobby
        queueSize.append(sum(eachQueueSize[j][-1] for j in eachQueueSize.keys())) 
        
        # length of overall lobby queue
        lenLobbyQueue = queueSize[-1]
        # Are there empty elevators in the lobby and unserved pax in the queue
        if (any(elevDict['LobbyState'].values()) and lenLobbyQueue>0): 
            # list of available elev
            availableElev = [j for j in elevDict['LobbyState'].keys() if elevDict['LobbyState'][j] == True]
            # initialize a list of pax who board the elevators
            elevPax = dict.fromkeys(availableElev,[]) 
            # initialize a list of the destinations of pax who board the elevators
            elevPaxDest =  dict.fromkeys(availableElev,[])
            # this will iterate over waiting pax in the line, this is an index for unserved pax.
            indexTotalLobbyQueue = 0
            # how many times are we cycling through each queue
            cycling = 0 

            # while there are available elevators and we haven't cycled
            # through all the queues without any action
            while (len(availableElev)>0) and (cycling < numQueues): 
                # if the current queue is empty
                if (not any(lobbyQueue[whichQueue])): 
                    # Move to next queue
                    whichQueue = (whichQueue+ 1)%numQueues 
                    # cycle once more
                    cycling += 1
                else:
                    # Take the group of pax at head of whichQueue
                    someGroupPax = FirstNpax(lobbyQueue[whichQueue],elevCap).copy() 
                    # first pax in this group
                    groupLeader = someGroupPax[0] 
                    # dest of groupLeader
                    groupLeaderDest = paxDict['Dest'][groupLeader] 
                    # find a feasible elevator
                    feasibleElev = [j for j in availableElev if groupLeaderDest in elevDict['SoftConstr'][j]] 
                
                     # if no feasible elev, move to next queue
                    if not any(feasibleElev):
                        # cycle once more
                        cycling += 1
                    else:
                        # pick first feasible elevator
                        elevIndex = feasibleElev[0]
                        # reset cycling to 0 since we are going to load an elev
                        cycling = 0
                        # these pax will board this elevator
                        elevPax[ elevIndex ] = someGroupPax.copy() 
                        # add destination of these pax
                        elevPaxDest[ elevIndex ] = [paxDict['Dest'][j] for j in someGroupPax] 
                        # current load of this elevator
                        currLoad = len(someGroupPax)
                        for j in range(0,currLoad,1):
                            # Remove this group of pax from whichQueue
                            del lobbyQueue[whichQueue][0] 
                        
                        # another cycling variable to fill up remaining elev capacity
                        cycling2=0
                        # while this elev is not yet full and we haven't cycled
                        # through all the queues without any action
                        while (currLoad<elevCap) and (cycling2<numQueues):
                            # move to next queue
                            whichQueue = (whichQueue+ 1)%numQueues 
                            # if the current queue is not empty
                            if any(lobbyQueue[whichQueue]):
                                # Take the group of pax at head of whichQueue
                                remGroupPax = FirstNpax(lobbyQueue[whichQueue],elevCap-currLoad).copy()
                                # first pax in this group
                                remGroupLeader = remGroupPax[0] 
                                # dest of groupLeader
                                remGroupLeaderDest = paxDict['Dest'][remGroupLeader] 
                                # if this destination is served by the elevator
                                if remGroupLeaderDest in elevDict['SoftConstr'][elevIndex]:
                                     # This group will also board this elevator
                                    elevPax[ elevIndex ] += remGroupPax.copy() 
                                     # adding their destinations
                                    elevPaxDest[ elevIndex ] += [paxDict['Dest'][j] for j in remGroupPax] 
                                     # update load of this elevator
                                    currLoad += len(remGroupPax)
                                    for j in range(0,len(remGroupPax),1):
                                         # Remove this group of pax from whichQueue
                                        del lobbyQueue[whichQueue][0] 
                            # cycle once more             
                            cycling2 += 1       
                         
                        # elevator is full, so it could leave the lobby
                        elevDict['LobbyState'][elevIndex] = False
                        # update waiting time of the pax
                        paxDict = UpdatePaxWaitTime(paxDict,elevPax[elevIndex],elevIndex,elevDict)
                        # calculate trip times of the pax
                        tripTimes = PaxTripTime(elevPax[elevIndex],elevPaxDest[elevIndex],elevInfo)
                         # these many pax in current lobby have been served
                        indexTotalLobbyQueue += len(elevPax[elevIndex])
                        
                        # Update trip times of pax
                        for j in range(len(elevPax[elevIndex])): 
                            paxDict['TripTime'][elevPax[elevIndex][j]] = tripTimes[j]
                        # update number of button presses (stops) made in this elevator
                        buttonPress += [len(set(elevPaxDest[elevIndex]))]
                        # calculate round trip time of this elev
                        roundTripTime = RoundTripTime(elevPaxDest[elevIndex],elevInfo)
                        # update next time this elev returns to the lobby
                        elevDict['NextLobby'][elevIndex] = currTime + roundTripTime #update next lobby time for that eleavtor
                        # this elev is removed from list of available elev
                        availableElev.remove(elevIndex)
                        # update list of loads 
                        loadSize.append(elevCap)
                    # move to next queue
                    whichQueue = (whichQueue+ 1)%numQueues 
 
    return (list(paxDict['WaitingTime'].values()),queueSize, loadSize, list(paxDict['TripTime'].values()),buttonPress,eachQueueSize) 



#######################################################################
"""
Functions that compare across interventions, run multiple simulations etc.
"""

"""
This function evaluates all interventions for each arrival sequence and 
computes the output metrics for them

Parameters:
paxInfo: contains passenger configurations
elevInfo: contains configurations of elevators in the building
IntervList: list of interventions we wish to compare

Output: an implementation of all the interventions, with the following outputs:
Waiting time of all pax, queue size over time, list of loads of elevators,
list of trip times of all pax, number of stops on each elevator trip.
The output is a dictionary with the metrics for each intervention.   
"""
def run_compareInterv(paxInfo, elevInfo, IntervList):

    # total number of floors, upper bound on pax destinations
    numFloor = elevInfo[0] 
    # total number of elevators
    elevNumTotal = elevInfo[1] 
    # speed of elevator to traverse one floor
    elevSpeed = elevInfo[2]  
    # down multiplier to account for intermediate pax entering and leaving
    elevSpeedMultiplier = elevInfo[3]  
    # time to board an elevator, depends on num of pax entering
    elevBoardTime = elevInfo[4] 
    # time to deboard an elevator, depends on num of pax leaving
    elevStopTime = elevInfo[5] 
    # capacity of each elevator
    elevCap = elevInfo[7] 
    
    timeInterval = 10
    
    # all csv file paths
    all_files = paxInfo[0]
    # the number of simulations we run and average over
    numFile = paxInfo[1]
    # list of WtW  
    qList = paxInfo[3]
    # the number of queues, if we are performing queue splitting
    numQueues = len(paxInfo[2])
    # the floor ranges of each queue, if we are performing queue splitting
    queueDest = paxInfo[2]
    
    
#     IntervList = ["split4","CohortSplit4"] #["FCFS", "CohortFCFS", "split","CohortSplit","split4","CohortSplit4", "FCFSQueueSplit"]
    CohortIntervList = ["CohortFCFS","CohortSplit","CohortSplit4"]
    resultDict =  {} 
    resultDict['waitTime']=dict.fromkeys(qList,{}) #times when elevator is at the lobby
    resultDict['Load'] = dict.fromkeys(qList,{}) #any hard constraints for the elevator, e.g. floors 1-15 only
    resultDict['Queue']=dict.fromkeys(qList,{}) # binary- is the elevator in the lobby right now?
    resultDict['TripTime'] = dict.fromkeys(qList,{})
    resultDict['Button']= dict.fromkeys(qList,{})
    
    # for each WtW
    for q in qList:
        for key in resultDict.keys():
            resultDict[key][q] = dict.fromkeys(IntervList,[])
            
    for q in qList:
        # for each of the 100 simulation files
        for file in all_files[str(q)]:
            for intervention in IntervList:
                
                paxDict =  createPaxDict(file,numFloor)
                # create elevator dictionary with hard & soft constraint
                elevDict = createElevDict(elevNumTotal, elevInfo[6]) 
                # print(elevDict['SoftConstr'])
                if intervention in CohortIntervList:
                    (waitTime,queue,load, tripTime, button) = ElevIntervCohorting(elevDict,paxDict,elevInfo)
#                     ElevIntervCohorting(elevDict,paxDict,elevSpeed,elevSpeedMultiplier,elevBoardTime, elevStopTime,elevNumTotal,elevCap)
                
                elif (intervention == "FCFSQueueSplit"):
                   
                    (waitTime,queue,load, tripTime, button,eachQueueSize) = ElevIntervQueueSplitwithWalking(elevDict,paxDict,elevInfo,paxInfo)
                    #(elevDict,paxDict,elevSpeed,elevSpeedMultiplier,elevBoardTime,elevStopTime,elevNumTotal,elevCap,4)
                else:
                    (waitTime,queue,load, tripTime, button) = ElevIntervSoftConstr(elevDict,paxDict,elevInfo)
                    
                # append the results into the resultDict
                resultDict['waitTime'][q][intervention]= resultDict['waitTime'][q][intervention] + [[np.average(list(waitTime)),np.std(list(waitTime)),np.max(list(waitTime)) ]]
                resultDict['Queue'][q][intervention]=resultDict['Queue'][q][intervention]+ [[np.average(list(queue)),np.std(list(queue)),np.max(list(queue)) ]]
                resultDict['Load'][q][intervention]=resultDict['Load'][q][intervention] + [[np.average(list(load)),np.std(list(load)),np.max(list(load)) ]]
                resultDict['TripTime'][q][intervention]=resultDict['TripTime'][q][intervention] +[[np.average(list(tripTime)),  np.std(list(tripTime)),np.max(list(tripTime))]]
                resultDict['Button'][q][intervention]=resultDict['Button'][q][intervention] +[[np.average(list(button)),  np.std(list(button)),np.max(list(button))]]

    return resultDict


"""
This function, given an intervention performs multiple simulations and outputs
the results of the intervention

Parameters:
paxInfo: contains passenger configurations
elevInfo: contains configurations of elevators in the building
Interv: the intervention we wish to analyze

Output: an implementation of the intervention, across many simulations:
Waiting time of all pax, queue size over time, list of loads of elevators,
list of trip times of all pax, number of stops on each elevator trip.  
"""
def run_InterventionOnMultipleFiles(paxInfo, elevInfo, intervention):
    # total number of floors, upper bound on pax destinations
    numFloor = elevInfo[0] 
    # total number of elevators
    elevNumTotal = elevInfo[1] 
    # speed of elevator to traverse one floor
    elevSpeed = elevInfo[2]  
    # down multiplier to account for intermediate pax entering and leaving
    elevSpeedMultiplier = elevInfo[3]  
    # time to board an elevator, depends on num of pax entering
    elevBoardTime = elevInfo[4] 
    # time to deboard an elevator, depends on num of pax leaving
    elevStopTime = elevInfo[5] 
    # service range of elevator
    elevServiceRange = elevInfo[6]
    # capacity of each elevator
    elevCap = elevInfo[7]   
    # we update the system every 10 seconds
    timeInterval = 10
    # all csv file paths
    all_files = paxInfo[0]
    # the number of simulations we run and average over
    numFile = paxInfo[1]
    # the WtW parameter 
    WtW = paxInfo[3]
    # the number of queues, if we are performing queue splitting
    numQueues = len(paxInfo[2])
    # the floor ranges of each queue, if we are performing queue splitting
    queueDest = paxInfo[2]
    
    # output metrics over multiple simulations
    # wait time of pax
    multiWaitTime = [] 
    # elev loads
    multiLoad = [] 
    # avg queue length over the simulations
    multiAvgQueue = [] 
    # queue length over time
    multiTimeQueue = []
    # trip time of pax
    multiTripTime = []
    # number of buttons pressed= number of stops made in each elevator trip
    multiButtonPress = []

    # avg queue length of each queue, if we are performing queue splitting
    multiAvgEachQueue = {k: [] for k in range(numQueues)}
    # queue length over time of each queue, if we are performing queue splitting
    multiTimeEachQueue = {k: [] for k in range(numQueues)}

    # for each simulation
    # track which simulation we are in (out of 100)
    index = 0
    for filename in all_files:
        
        # if it is any of the following interventions, which use cohorting
        if intervention in ['CohortFCFS',"CohortSplit","CohortSplit4","CohortLongChain","CohortDedicate"]:
            # create dict for pax
            paxDict =  createPaxDict(filename,numFloor)
            # create elevator dictionary with hard & soft constraint
            elevDict = createElevDict(elevNumTotal , elevServiceRange) 
            # run the intervention
            (waitTime,queue,load, tripTime, button) = ElevIntervCohorting(elevDict,paxDict,elevInfo)
            # append the results into the output
            # store wait time
            multiWaitTime = AddTwoLists(multiWaitTime,waitTime)
            # store the queue length over time
            multiTimeQueue = AddTwoLists(multiTimeQueue,queue)
            # store the average queue
            multiAvgQueue += queue
            # store the load
            multiLoad += load
            # store the trip time of pax
            multiTripTime += tripTime
            #multiTripTime = AddTwoLists(multiTripTime,tripTime)
            # store the number of elev stops/button press
            multiButtonPress += button
        
        # if the intervention is queue splitting    
        elif (intervention == 'FCFSQueueSplit'):
            # create dict for pax
            paxDict =  createPaxDict(filename,numFloor)
            # create elevator dictionary with hard & soft constraint
            elevDict = createElevDict(elevNumTotal , elevInfo[6]) 
            # run the intervention
            (waitTime,queue,load, tripTime, button,eachQueueSize) = ElevIntervQueueSplit(elevDict,paxDict,elevInfo,paxInfo)
            
            # append the results into the output
            # store wait time
            multiWaitTime = AddTwoLists(multiWaitTime,waitTime)
            # store the queue length over time
            multiTimeQueue = AddTwoLists(multiTimeQueue,queue)
            # store the average queue
            multiAvgQueue += queue
            # store the load
            multiLoad += load
            # store the trip time of pax
            multiTripTime += tripTime
            # multiTripTime = AddTwoLists(multiTripTime,tripTime)
            # store the number of elev stops/button press
            multiButtonPress += button
            
            # we also track the size of each queue, both average and versus time
            for whichQueue in range(numQueues):
                multiAvgEachQueue[whichQueue] += eachQueueSize[whichQueue]
                multiTimeEachQueue[whichQueue] = AddTwoLists(multiTimeEachQueue[whichQueue],eachQueueSize[whichQueue])
                
        # for all other interventions    
        else:
            # create dict for pax
            paxDict =  createPaxDict(filename,numFloor)
            # create elevator dictionary with hard & soft constraint
            elevDict = createElevDict(elevNumTotal,elevServiceRange) 
            # run the intervention
            (waitTime,queue,load, tripTime, button) = ElevIntervSoftConstr(elevDict,paxDict,elevInfo)
                   
            # append the results into the output
            # store wait time
            multiWaitTime = AddTwoLists(multiWaitTime,waitTime)
            # store the queue length over time
            multiTimeQueue = AddTwoLists(multiTimeQueue,queue)
            # store the average queue
            multiAvgQueue += queue
            # store the load
            multiLoad += load
            # store the trip time of pax
            multiTripTime += tripTime
            # multiTripTime = AddTwoLists(multiTripTime,tripTime)
            # store the number of elev stops/button press
            multiButtonPress += button
        # print which simulation we are running, so we know where we are at
        index += 1
        print(index)
        
    # This will average across numFile and return the intervention outputs
    # for waitTime, we simply average     
    multiWaitTime = list(np.array(multiWaitTime,dtype='f')/numFile)
    # for finding the result of an "average" simulation, we use the function
    # AverageALargeList, which yields what a typical simulation looks like
    multiAvgQueue = AverageALargeList(multiAvgQueue,numFile,range(max(multiAvgQueue)))
    # for finding queue length over time, we simply average
    multiTimeQueue = list(np.array(multiTimeQueue,dtype='f')/numFile)
    # for trip time of pax, we simply average
   # multiTripTime = list(np.array(multiTripTime,dtype='f')/numFile)
    
    # for the queue split intervention, we also compute length of each queue
    if (intervention == 'FCFSQueueSplit'):
        # for each queue in queue split
        for whichQueue in range(numQueues):
            d = list(multiAvgEachQueue[whichQueue])
            # for finding the result of an "average" simulation, we use the function
            # AverageALargeList, which yields what a typical simulation looks like
            multiAvgEachQueue[whichQueue] = AverageALargeList(d,numFile,range(max(d)))
            # for finding queue length over time, we simply average
            multiTimeEachQueue[whichQueue] = list(np.array(list(multiTimeEachQueue[whichQueue]),dtype='f')/numFile)
    
    # For other two, multiLoad and multiButtonPress, we concatenate all arrays
    # and the compute the average
    multiLoad = AverageALargeList(multiLoad,numFile,list(range(1,elevCap+1,1)))
    multiButtonPress = AverageALargeList(multiButtonPress,numFile,list(range(1,elevCap+1,1)))
            
    return (multiWaitTime,multiAvgQueue,multiTimeQueue,multiLoad,multiTripTime,multiButtonPress,multiAvgEachQueue,multiTimeEachQueue)


# this function evaluates numFile filesfor each intervention compute the waitTime, queue length, load, trip time, etc.
# the input is elevator capacity, intervention, numbber of files, walkability percentage
# the output is a dictionary: each metric to each intervention to a list of list
# Example: result = run_interventionOnMultipleFiles(2,FCFS,100,20)
# IntervList = ["FCFS", "CohortFCFS", "split","CohortSplit","split4","CohortSplit4"]

"""
This function, given an intervention performs multiple simulations and outputs
the results of the intervention- spefifically for limited cohorting

Parameters:
paxInfo: contains passenger configurations
elevInfo: contains configurations of elevators in the building
Interv: the intervention we wish to analyze

Output: an implementation of the intervention, across many simulations:
Waiting time of all pax, queue size over time, list of loads of elevators,
list of trip times of all pax, number of stops on each elevator trip.  
"""
def run_interventionOnMultipleFiles_LimitedCohort(paxInfo, elevInfo, intervention, lobbySize, cohortSize):

    numFloor = elevInfo[0] # total number of floors, upper bound on pax destinations
    elevNumTotal = elevInfo[1]  # total number of elevators
    elevSpeed = elevInfo[2]  # speed of elevator to traverse one floor
    elevSpeedMultiplier = elevInfo[3]  # multiplier to account for intermediate pax entering and leaving
    elevBoardTime = elevInfo[4] # time to board an elevator, depends on num of pax entering
    elevStopTime = elevInfo[5] 
    elevCap = elevInfo[7]
    timeInterval = 10
    all_files = paxInfo[0]
    numFile = paxInfo[1]
    WtW = paxInfo[3]
    numQueues = len(paxInfo[2])
    elevServiceRange = elevInfo[6]  
    timeInterval = 10
    #     IntervList = ["FCFS","CohortFCFS","split","CohortSplit","split4","CohortSplit4", "LongChain","CohortLongChain","dedicate"]

    multiWaitTime = [] #times when elevator is at the lobby
    multiLowWaitTime = []
    multiHighWaitTime = []
    multiLoad = [] #any hard constraints for the elevator, e.g. floors 1-15 only
    multiAvgQueue = [] # binary- is the elevator in the lobby right now?
    multiTimeQueue = []
    multiTripTime = []
    multiButtonPress = []

    multiAvgEachQueue = {k: [] for k in range(4)}
    multiTimeEachQueue = {k: [] for k in range(4)}

    for filename in all_files:
        elevDict = createElevDict(elevNumTotal, elevServiceRange)
        paxDict =  createPaxDict(filename,numFloor)
        if intervention in ['CohortFCFS',"CohortSplit","CohortSplit4","CohortLongChain","CohortDedicate", "Pairing"]:
            (waitTime,queue,load, tripTime, button) = ElevIntervLimitedCohorting(elevDict,paxDict,elevInfo,lobbySize,cohortSize)
               
            lowWaitTime = [waitTime[i]  for i in range(len(waitTime))if paxDict['Dest'][i]<=15] 
            highWaitTime = [waitTime[i]  for i in range(len(waitTime))if paxDict['Dest'][i]>=16]
            
            # append the results into the resultDict
            multiWaitTime = AddTwoLists(multiWaitTime,waitTime)
            multiLowWaitTime += [np.average(lowWaitTime)]
            multiHighWaitTime += [np.average(highWaitTime)]
            multiTimeQueue = AddTwoLists(multiTimeQueue,queue)
            multiAvgQueue += queue
            multiLoad += load
            multiTripTime = AddTwoLists(multiTripTime,tripTime)
            multiButtonPress += button
            
        else:
            print('The input intervention is not cohorting. Please check the intervention')

    # This will average across 100 files and return        
    multiWaitTime = list(np.array(multiWaitTime,dtype='f')/numFile)
    avgLowWaitTime = np.average(multiLowWaitTime)
    avgHighWaitTime = np.average(multiHighWaitTime)
    multiAvgQueue = AverageALargeList(multiAvgQueue,numFile,range(max(multiAvgQueue)))
    multiTimeQueue = list(np.array(multiTimeQueue,dtype='f')/numFile)
    multiTripTime = list(np.array(multiTripTime,dtype='f')/numFile)
    
    if (intervention == 'FCFSQueueSplit'):
        for whichQueue in range(4):
            d = list(multiAvgEachQueue[whichQueue])
            multiAvgEachQueue[whichQueue] = AverageALargeList(d,numFile,range(max(d)))
            multiTimeEachQueue[whichQueue] = list(np.array(list(multiTimeEachQueue[whichQueue]),dtype='f')/numFile)
    
    # For other two, multiLoad and multiButtonPress, we concatenate all arrays
    #  so average and create a new list which reflects them over 
    multiLoad = AverageALargeList(multiLoad,numFile,[1,2,3,4])
    multiButtonPress = AverageALargeList(multiButtonPress,numFile,[1,2,3,4])
            
    return (multiWaitTime,avgLowWaitTime,avgHighWaitTime,multiAvgQueue,multiTimeQueue,multiLoad,multiTripTime,multiButtonPress,multiAvgEachQueue,multiTimeEachQueue)


#################################################################################