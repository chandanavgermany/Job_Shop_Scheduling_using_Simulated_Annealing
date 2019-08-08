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
import matplotlib.patches as mpatches

class Utilities:
    
    # Generate the random solution
    def generate(self,numberOfJobs, numberOfMachines):
        generate = [i for i in list(range(numberOfJobs)) for _ in range(numberOfMachines)]
        random.shuffle(generate)
        return generate
    
    # Get the neighbors of the current state
    # Mode = Normal: Swap an element with immediate neighbor
    # Mode = Random or Others: Swap an element with a randomnly selected element
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
    
    # Create an initial solution
    def getInitialSolution(self, jobshopLoaderObj):
        jobs = jobshopLoaderObj.jobs_list()
        initialSolution = 0
        for i in range(jobshopLoaderObj.numberOfJobs()):
            for j in range(jobshopLoaderObj.numberOfOperations()):
                initialSolution+= jobs[i][j][1]
        return initialSolution
    
    # To obtain the cost of each sequence
    # Cost is the amount of time taken to execute all the operations of every job given
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
    
    # To plot the best solution using the plot in matplotlib
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
        
        colors, colorPatches = self.get_colors(numberOfOperations)
        for i in solution:
            machine, time = jobs[i][iterationVar[i]]
            iterationVar[i] += 1
            start = max(time_Jobs[i], time_Operations[machine])
            end = start + time
            time_Jobs[i] = end
            time_Operations[machine] = end
            print(time_Jobs)
            # Initialiasing the plot
            if m == 0:
                plt.bar(index,tuple(time_Jobs), width, color = colors[machine])  
                new_state = time_Jobs[:]
                old_state = new_state[:]
            # Add the stacked bar for each job on the initialised plot
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
                    plt.bar(index, tuple(new_state), width, bottom=old_state, color = (1,1,1,1),)
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
        plt.xlabel('Jobs')
        plt.ylabel('Time in seconds')
        legend_x = 1
        legend_y = 0.5
        plt.legend(handles=colorPatches, title = 'Machines', loc='center left', bbox_to_anchor=(legend_x, legend_y))      
        plt.show()
    
    # To create unique colors for plotting for different machines
    def get_colors(self, num_colors):    
        colors=[]
        colorPatches=[]
        j = 0
        for i in np.arange(0., 360., 360. / num_colors):
            hue = i/360.
            lightness = (50 + np.random.rand() * 10)/100.
            saturation = (90 + np.random.rand() * 10)/100.
            color = colorsys.hls_to_rgb(hue, lightness, saturation)
            colors.append(color)
            patch = mpatches.Patch(color=color, label='M' + str(j))
            colorPatches.append(patch)
            j += 1
        return colors, colorPatches
            
