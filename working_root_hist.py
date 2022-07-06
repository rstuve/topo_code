"""
June 26, 2022
Author: Ryan Stuve

Moves transverse energy data from root file to array,
presents it as histogram using matplotlib.pyplot

All lines with FILE DEPENDENT need to be reviewed and edited if used
with other files besides user.bochen.25650990.OUTPUT._000001.root
"""
from ROOT import *
import numpy as np
import matplotlib.pyplot as plt

cycle = '2' # choose branch of data, FILE DEPENDENT
v = True # print updates to stdout as script runs
layer = 1

if v:
    print('Preprocessing...')

f = TFile('../data/user.bochen.25650990.OUTPUT._000001.root') # FILE DEPENDENT
tree = f.Get("SCntuple;"+cycle) # FILE DEPENDENT
numEntries = tree.GetEntries()

def printProgress(event):
    checkpoint = numEntries // 100
    if event % checkpoint == 0:
        progress = int(event/checkpoint)
        print("Loading: [{:<10s}] {}% complete".format('▭'*int(progress / 10), progress), end='\r')


Et = [] # array to store Et values
for event in range(numEntries):
    tree.GetEntry(event)
    EtT = tree.scells_Et # FILE DEPENDENT
    for value in EtT:
        Et.append(value)
    if v:
        printProgress(event)

if v:
    print("Converting data")
if v:
    print("Data processed, creating histogram...")
Et = np.asarray(Et)
plt.hist(Et, bins=20, range=(0,1000)) # Range is FILE DEPENDENT
plt.title("scells_Et_Cycle_"+cycle)
plt.xlabel("Tranverse Energy (Mev)")
plt.ylabel("Counts / 50 MeV")
plt.show()
