#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 30 08:51:35 2019

@author: chandanav
"""

class JobShopLoader:
    jobs = []
    jobShop = []
    
    def load(self, file_name):
        inputfile = open(file_name, "r")
        jobs_list = list()
        for line in inputfile:
            line = line.strip()
            self.jobShop.append(line)
            job = [(int(machine), int(operationTime)) for machine, operationTime in zip(*[iter(line.split())]*2)]
            jobs_list.append(job)
        self.jobs = jobs_list[:]
        return self.jobs
    
    def numberOfOperations(self):
        return len(self.jobs[0])
    
    def numberOfJobs(self):
        return len(self.jobs)
    
    def jobs_list(self):
        return self.jobs
    
    def printJobMatrix(self):
        print(str(self.numberOfJobs()) + ' * ' + str(self.numberOfOperations()))
        for i in self.jobShop:
            print(i)
    