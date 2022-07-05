"""
June 26, 2022
Author: Ryan Stuve

Moves transverse energy data from root file to array,
presents it as histogram using matplotlib.pyplot

Required to be in same directory as root file

All lines with FILE DEPENDENT need to be reviewed and edited if used
with other files besides user.bochen.25650990.OUTPUT._000001.root
"""
from ROOT import *
import numpy as np
import matplotlib.pyplot as plt

cycle = '2' # choose branch of data, FILE DEPENDENT
v = False # print updates to stdout as script runs
layer = 1

etaSet = 1.4 # max eta value
etaGran = .125 # eta granularity
phiSet = 3.1 # max phi
phiGran = .2
binSize = 50
max = 1000

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
for event in range(1):#numEntries):
    tree.GetEntry(event)
    Ets = tree.scells_Et # FILE DEPENDENT
    samples = tree.scells_sampling
    etas = (np.asarray(tree.scells_eta) + etaSet) // etaGran
    phis = (np.asarray(tree.scells_phi) + phiSet) // phiGran
    l = [(tuple[1:]) for tuple in zip(samples,etas,phis,Ets) if tuple[0] == 1]
    l.sort()
    eta_i = 0
    phi_i = 0
    currentV = 0
    matches = 0

    for tuple in l:
        if tuple[0] == eta_i: # if same eta
            if tuple[1] == phi_i: # if same phi
                currentV += tuple[2]
                matches += 1
            else:
                if currentV != 0:
                    Et.append(currentV)
                phi_i = tuple[1]
                currentV = tuple[2]
        elif 0 < tuple[0] <= int(etaSet*2//etaGran):
            if currentV != 0:
                Et.append(currentV)
            eta_i = tuple[0]
            phi_i = tuple[1]
            currentV = tuple[2]

    if currentV != 0:
        Et.append(currentV)

    if v:
        printProgress(event)

if v:
    print("Converting data")
if v:
    print("Data processed, creating histogram...")
Et = np.asarray(Et)
print(matches)
print(len(Et))
hist, bins = np.histogram(Et, bins = int(max/binSize), range=[0,max])

b = (bins[:-1] + bins[1:])/2
np.savez('../data/npfile.npz', hist)
plt.plot(b,hist, ds = 'steps')
#plt.hist(Et, bins=20, range=(0,1000)) # Range is FILE DEPENDENT
#plt.title("scells_Et_Cycle_"+cycle)
#plt.xlabel("Tranverse Energy (Mev)")
plt.show()
