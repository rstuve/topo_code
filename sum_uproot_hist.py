"""
July 5, 2022
Author: Ryan Stuve

Converts transverse energy data from root file to awkward array,
presents it as histogram using matplotlib.pyplot

Required to be in same directory as root file

All lines with FILE DEPENDENT need to be reviewed and edited if used
with other files besides user.bochen.25650990.OUTPUT._000001.root
"""
import uproot
import matplotlib.pyplot as plt
import numpy as np

cycle = '2' # cycle being analyzed, FILE DEPENDENT
layer = 1

etaSet = 1.4 # max eta value
etaGran = .125 # eta granularity
phiSet = 3.1 # max phi
phiGran = .2

# Extract data from root file
fileName = "../data/user.bochen.25650990.OUTPUT._000001.root" #FILE DEPENDENT
file = uproot.open(fileName)
tree = file["SCntuple;"+cycle]  #FILE DEPENDENT
branches = tree.arrays()
Et = []



for event in range(len(branches)):
    grid = np.zeros((len(np.arange(-etaSet,etaSet,etaGran)), len(np.arange(-phiSet,phiSet,phiGran))))
    e = branches[event]
    #samples = np.asarray(e['scells_sampling'])
    #indices = np.where(samples == layer)
    #etaList = e['scells_eta'][indices]
    #phiList = e['scells_phi'][indices]
    #EtT = e["scells_Et"][indices]


    #for i in range(len(EtT)):
    #    if -etaSet < etaList[i] < etaSet:
    #        grid[int((etaList[i]+etaSet)//etaGran)][int((phiList[i]+phiSet)//phiGran)] += EtT[i]
    if event % 100 == 0:
        print('Loading: {}%'.format(event/100), end='\r')
    #for item in grid[np.nonzero(grid)]:
    #    Et.append(item)
quit()

# Plot and display data
data = np.asarray(Et)
plt.hist(data, bins = 100, range = (0,1000)) # ends cut off, FILE DEPENDENT

plt.title("scells_Et_Cycle_"+cycle+', layer '+str(layer)) # FILE DEPENDENT
plt.xlabel("Tranverse Energy (Mev)")
plt.show()
