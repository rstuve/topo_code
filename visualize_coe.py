"""
Author: Ryan Stuve
Date modified: 7/1/2022

Presents .coe file as visual graph of energies
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Get file and data
run_folder = '2022_07_06-h14-m00-s07_SCntuple;2' # change based off location of event
event = 0
layer = 1

currentDir = os.getcwd()
path = '../data/root_to_coe/' + run_folder + '/by_event/event_' + str(event) + '/'
filename = 'Cell_EtsLayer'+str(layer)+'.coe'
with open(path+filename) as f:
    lines = f.readlines()

#== get info from header ===============
header = lines[0]
bit_size = int(header[137:])
etaSet = float(header[73:76]) # max eta value, 3 digits including decimal
etaGran = float(header[84:89]) # eta granularity, 5 digits
phiSet = float(header[108:111]) # max phi, 3 digits
phiGran = float(header[119:122]) # 3 digits
print(bit_size, etaSet, etaGran, phiSet, phiGran) # test values

# Move data into np.array
Ets = np.empty((0,int(len(lines[4].strip())/bit_size)))
for line in lines[3:]:
    dataString = line.strip()
    EtT = [int(dataString[i:i+bit_size], 2) for i in range(0, len(dataString), bit_size)]
    Ets = np.append(Ets, np.array([EtT]), axis=0)

if not np.any(Ets): # if there are no values besides 0s
    raise ValueError("plot requires at least 1 Et value")

#== Plot np.array =================
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(Ets, norm = LogNorm(),extent=[-phiSet,phiSet,etaSet,-etaSet])
plt.xlabel('$\phi$')
plt.ylabel('$\eta$')
plt.title("Event "+str(event)+', Layer '+str(layer),y = 1.2, pad=30,fontweight="bold")
cb = fig.colorbar(cax)
cb.set_label('MeV', rotation = 0, loc = 'bottom')

plt.show()
