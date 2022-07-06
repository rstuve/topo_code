"""
June 26, 2022
Author: Ryan Stuve

Moves ET data for all layers in one event from root file to array,
presents it as histogram using matplotlib.pyplot
"""
from ROOT import *
import numpy as np
import matplotlib.pyplot as plt

event = 0 # choose event
cycle = '2' # choose branch of data

f = TFile('../data/user.bochen.25650990.OUTPUT._000001.root')
tree = f.Get("SCntuple;"cycle)

Et = [] # array to store Et values
tree.GetEntry(event)
EtT = tree.scells_Et
for value in EtT:
    Et.append(value)

Et = np.asarray(Et)
plt.hist(Et, bins=20, range=(0,1000)) # Range is FILE DEPENDENT
plt.title("scells_Et_Cycle_"+layer)
plt.xlabel("Tranverse Energy (Mev)")
plt.ylabel("Counts")
plt.show()
