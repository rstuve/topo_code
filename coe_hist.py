"""
Author: Ryan Stuve
Date modified: 6/27/2022

Takes a folder from current directory of .coe files, extracting ET data 
and plotting it as a histogram """

import numpy as np
import matplotlib.pyplot as plt
import os

folder_name = input("Folder name: \n> ") # Name of folder holding all the coe values
layer_num = folder_name[-1]
path_name = 'root_to_coe/' + folder_name + '/Et_values/' # might depend on current directory
numOfEvents = len(os.listdir(path_name)) # make sure there are no other files saved


def bin_to_dec(num):
    'changes binary string to decimal number'
    return int(num,2)

def printProgress(event):
    'visual progress bar on stdout during runtime'
    checkpoint = numOfEvents // 100
    if event % checkpoint == 0:
        progress = int(event/checkpoint)
        print("Loading: [{:<10s}] {}% complete".format('▭'*int(progress / 10), progress), end='\r')


a = [] # array used to collect decimal values

for event in range(numOfEvents): # loop through files
    printProgress(event)
    with open(path_name + '_input_data_et_event' + str(event) + '.coe') as f:
        data = f.readlines()
        for d in data:
            a.append(bin_to_dec(d.strip()))

a = np.asarray(a)
print("Data processed, generating histogram...")
plt.hist(a, bins=100, range=(0,100)) # Range is FILE DEPENDENT
plt.title("scells_Et_Cycle_"+layer_num)
plt.xlabel("Tranverse Energy (.01 Gev)")
plt.show()
