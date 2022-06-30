"""
June 23, 2022
Author: Ryan Stuve

Converts transverse energy data from root file to awkward array,
presents it as histogram using matplotlib.pyplot


All lines with FILE DEPENDENT need to be reviewed and edited if used
with other files besides user.bochen.25650990.OUTPUT._000001.root
"""
import uproot
import matplotlib.pyplot as plt
import awkward as ak

layer = input("Which layer? (enter 1 or 2):\n> ") # layer being analyzed, FILE DEPENDENT

# Extract data from root file
fileName = "../data/user.bochen.25650990.OUTPUT._000001.root" #FILE DEPENDENT
file = uproot.open(fileName)
tree = file["SCntuple;"+layer]  #FILE DEPENDENT
branches = tree.arrays()
data = branches["scells_Et"] # store as awkward array, FILE DEPENDENT

# Plot and display data
data = ak.flatten(data)
plt.hist(data, bins = 100, range = (0,1000)) # ends cut off, FILE DEPENDENT

plt.title("scells_Et_Cycle_"+layer) # FILE DEPENDENT
plt.xlabel("Tranverse Energy (Mev)")
plt.show()
