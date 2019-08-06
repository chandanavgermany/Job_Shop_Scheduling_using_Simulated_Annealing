#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 09:35:18 2019

@author: chandanav
"""
from Utilities import Utilities
import math, time, random
import matplotlib.pyplot as plt

class SimulatedAnnealing:
    
    def __init__(self):
        pass
    
    # To perform the search for the best solution for JobShop scheduling using the simulated annealing algorithm
    def simulatedAnnealingAlgorithm(self, jobshopLoaderObj, utilitiesObj, T, termination, halting, mode,shrink):
        currentState = utilitiesObj.generate(jobshopLoaderObj.numberOfJobs(), jobshopLoaderObj.numberOfOperations())
        for i in range(halting):
            # Calculate the temperature to facilitate avoiding local opt
            T = shrink * float(T)
            for j in range(termination):
                actualCost = utilitiesObj.getCost(jobshopLoaderObj, currentState)          
                
                for neighbor in utilitiesObj.getNeighbors(currentState, mode):
                    neighborCost = utilitiesObj.getCost(jobshopLoaderObj, neighbor)
                    probability = math.exp(-neighborCost / T)
                    
                    if (neighborCost < actualCost) or (random.random() < probability):
                        currentState = neighbor
                        actualCost = neighborCost
                            
        return currentState, actualCost
    
    # Search for the best solution
    def search(self, jobshopLoaderObj, utilitiesObj, maxTime = None, T = 200, termination = 10, halting = 10,mode = 'random', shrink = 0.8):
        solution = None
        numberofAttempts = 1
        scheduleLength = list()
        timeTaken = []
        best = utilitiesObj.getInitialSolution(jobshopLoaderObj)
        initialSolution = best
        time_t0 = time.time()
        total_attempts = 0
        
        while True:
            try:
                startTime = time.time()
                # Execute the search algorithm for given number of attempts
                for i in range(numberofAttempts):
                    newState, cost = self.simulatedAnnealingAlgorithm(jobshopLoaderObj, utilitiesObj, T, termination, halting, mode, shrink)
                    if cost < best:
                        best = cost
                        solution = (cost, newState)
                total_attempts += numberofAttempts
                
                # Stop the search algorithm which the time limit has been reached
                if maxTime and time.time()-time_t0 > maxTime:
                    raise Exception('Time limit is over')
                
                # Show the solution found at every attempt
                print("Best solution :"+  str(best) + " in " + str(time.time() - time_t0) + " sec")
                scheduleLength.append(best)
                timeTaken.append(time.time() - time_t0)
                t = time.time() - startTime
                
                # Modify the number of attempts based on the time taken to find one solution
                if t > 4:
                    numberofAttempts //= 2
                    numberofAttempts = max(numberofAttempts, 1)
                     
                elif t < 1.5:
                    numberofAttempts *= 2
            
            # Display the best solution found
            except: 
                jobshopLoaderObj.printJobMatrix()
                print("\n Initial Solution " + str(initialSolution))
                print("\n Best Solution")
                print(best)
                print(timeTaken)
                print(scheduleLength)
                plt.plot(timeTaken, scheduleLength)
                plt.xlabel("Time in sec")
                plt.ylabel('Operation cost')
                plt.show()
                return solution
                
                     
