#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 09:39:31 2019

@author: chandanav
"""
import random
import matplotlib.pyplot as plt
import numpy as np
import colorsys

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
    
    def showSolution(self, jobshopLoaderObj, solution):
        numberOfOperations = jobshopLoaderObj.numberOfOperations()
        numberOfJobs = jobshopLoaderObj.numberOfJobs()
        time_Operations = [0] * numberOfOperations
        time_Jobs = [0] * numberOfJobs
        iterationVar = [0] * numberOfJobs
        jobs = jobshopLoaderObj.jobs_list()
        index = np.arange(numberOfJobs)
        width = 0.3
        jobs_string = list()
        m = 0
        old_state = []
        new_state = []
        old_state_graph = []
        
        colors = self.get_colors(numberOfOperations)
        for i in solution:
            machine, time = jobs[i][iterationVar[i]]
            iterationVar[i] += 1
            start = max(time_Jobs[i], time_Operations[machine])
            end = start + time
            time_Jobs[i] = end
            time_Operations[machine] = end
            print(time_Jobs)
            if m == 0:
                plt.bar(index,tuple(time_Jobs), width, color = colors[machine])  
                new_state = time_Jobs[:]
                old_state = new_state[:]
            else:
                new_state = [a - b for a, b in zip(time_Jobs, old_state)]
                dif_num = 0
                position = 0
                for j in range(len(new_state)):
                    if new_state[j] != 0:
                        dif_num = new_state[j]
                        position = j
                        break
                if dif_num != time:
                    new_state[position] = dif_num - time
                    plt.bar(index, tuple(new_state), width, bottom=old_state, color = (1,1,1,1))
                    old_state = [a + b for a, b in zip(old_state, new_state)]
                    new_state[position] = time 
                    plt.bar(index, tuple(new_state), width, bottom = old_state, color = colors[machine])
                    old_state = [a + b for a, b in zip(old_state, new_state)]
                else:
                    plt.bar(index, tuple(new_state), width, bottom=old_state, color = colors[machine])
                    old_state = time_Jobs[:]
            m+=1
        for i in index:
            jobs_string.append('J '+str(i))
        plt.xticks(index, tuple(jobs_string))
        plt.show()
    

    def get_colors(self, num_colors):    
        colors=[]
        for i in np.arange(0., 360., 360. / num_colors):
            hue = i/360.
            lightness = (50 + np.random.rand() * 10)/100.
            saturation = (90 + np.random.rand() * 10)/100.
            colors.append(colorsys.hls_to_rgb(hue, lightness, saturation))
        return colors
            