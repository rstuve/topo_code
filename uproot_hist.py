"""
June 23, 2022
Author: Ryan Stuve

Converts transverse energy data from single layer of root file to array,
presents it as histogram using matplotlib.pyplot

does not group by eta or phi, see root_hist.py
"""
import uproot
import matplotlib.pyplot as plt
import numpy as np

cycle = '2' # cycle being analyzed, FILE DEPENDENT
layer = 1

# Extract data from root file
fileName = "../data/user.bochen.25650990.OUTPUT._000001.root" #FILE DEPENDENT
file = uproot.open(fileName)
tree = file["SCntuple;"+cycle]  #FILE DEPENDENT
branches = tree.arrays()
Et = []
for event in range(1):#len(branches)):
    e = branches[event]
    samples = np.asarray(e['scells_sampling'])
    indices = np.where(samples == layer)

    EtT = e["scells_Et"][indices]
    for value in EtT:
        Et.append(value)
    if event % 1000 == 0:
        print('Loading: '+str(event)[:2]+'%', end='\r')

# Plot and display data
data = np.asarray(Et)
plt.hist(data, bins = 100, range = (0,1000)) # ends cut off, FILE DEPENDENT

plt.title("scells_Et_Cycle_"+cycle+', layer '+str(layer)) # FILE DEPENDENT
plt.xlabel("Tranverse Energy (Mev)")
plt.show()
