#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 09:39:31 2019

@author: chandanav
"""
import random
class Utilities:
    
    def generate(self,numberOfJobs, numberOfMachines):
        generate = [i for i in list(range(numberOfJobs)) for _ in range(numberOfMachines)]
        random.shuffle(generate)
        return generate
    
    def getNeighbors(self, currentState, mode = "normal"):
        listOfNeighbors = list()
        for i in range(len(currentState) - 1):
            neighbor = currentState[:]
            if mode == "normal":
                swapIndex = i + 1
            else:
                swapIndex = random.randrange(len(currentState))
            neighbor[i], neighbor[swapIndex] = neighbor[swapIndex], neighbor[i]
            listOfNeighbors.append(neighbor)
        
        return listOfNeighbors
    
    def getInitialSolution(self, jobshopLoaderObj):
        jobs = jobshopLoaderObj.jobs_list()
        initialSolution = 0
        for i in range(jobshopLoaderObj.numberOfJobs()):
            for j in range(jobshopLoaderObj.numberOfOperations()):
                initialSolution+= jobs[i][j][1]
        return initialSolution
    
    def getCost(self, jobshopLoaderObj, newstate):
        numberOfOperations = jobshopLoaderObj.numberOfOperations()
        numberOfJobs = jobshopLoaderObj.numberOfJobs()
        time_Operations = [0] * numberOfOperations
        time_Jobs = [0] * numberOfJobs

        iterationVar = [0] * numberOfJobs
        jobs = jobshopLoaderObj.jobs_list()
        for i in newstate:
            machine, time = jobs[i][iterationVar[i]]
            iterationVar[i] += 1
            start = max(time_Jobs[i], time_Operations[machine])
            end = start + time
            time_Jobs[i] = end
            time_Operations[machine] = end
        return max(time_Operations)
    