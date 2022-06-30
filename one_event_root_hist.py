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

layer = input("Which layer? (enter 1 or 2):\n> ") # choose branch of data, FILE DEPENDENT

f = TFile('user.bochen.25650990.OUTPUT._000001.root') # FILE DEPENDENT
tree = f.Get("SCntuple;"+layer) # FILE DEPENDENT

Et = [] # array to store Et values
tree.GetEntry(0)
EtT = tree.scells_Et # FILE DEPENDENT
for value in EtT:
    Et.append(value)

Et = np.asarray(Et)
plt.hist(Et, bins=100, range=(0,1000)) # Range is FILE DEPENDENT
plt.title("scells_Et_Cycle_"+layer)
plt.xlabel("Tranverse Energy (Mev)")
plt.show()