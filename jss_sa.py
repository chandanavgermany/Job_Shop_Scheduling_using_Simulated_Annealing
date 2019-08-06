#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 09:01:40 2019

@author: chandanav
"""
from JobShopLoader import JobShopLoader
from Utilities import Utilities
from SimulatedAnnealing import SimulatedAnnealing
import matplotlib.pyplot as plt

# Initialization of the objects
jobshopLoader = JobShopLoader()
utilitiesObj = Utilities()
simulatedAnnealing = SimulatedAnnealing()

# Loading the data from the input file
jobs = jobshopLoader.load("data.txt")

# Calling the search algorithm to find the best solution for scheduling the jobs on machines
cost, solution = simulatedAnnealing.search(jobshopLoader, utilitiesObj, maxTime=20, T=200, termination=10, halting=10, mode='random',shrink = 0.8)

# Display the solution
utilitiesObj.showSolution(jobshopLoader, solution)
