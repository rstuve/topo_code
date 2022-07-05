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
run_folder = '2022_07_03-h17-m52-s08_SCntuple;2'
event = 0
layer = 1
bit_size = 10
etaSet = 1.4 # max eta value
etaGran = .125 # eta granularity
phiSet = 3.1 # max phi
phiGran = .2
currentDir = os.getcwd()
path = '../data/root_to_coe/' + run_folder + '/by_event/event_' + str(event) + '/'
filename = 'Cell_EtsLayer'+str(layer)+'.coe'
with open(path+filename) as f:
    lines = f.readlines()

# Move data into np.array
Ets = np.empty((0,int(len(lines[4].strip())/10)))
for line in lines[3:]:
    dataString = line.strip()
    EtT = [int(dataString[i:i+bit_size], 2) for i in range(0, len(dataString), bit_size)]
    Ets = np.append(Ets, np.array([EtT]), axis=0)

#Plot np.array
fig = plt.figure()
ax = fig.add_subplot(111)    # x is in axes-relative coordinates.
cax = ax.matshow(Ets, norm = LogNorm(),extent=[-phiSet,phiSet,-etaSet,etaSet])
plt.xlabel('$\phi$')
plt.ylabel('$\eta$')
plt.title("Event "+str(event)+', Layer '+str(layer),y = 1.2, pad=30,fontweight="bold")
fig.colorbar(cax)

#plt.matshow(Ets, vmin=0, vmax=int('1'*bit_size,2),extent=[-phiSet,phiSet,-etaSet,etaSet])
plt.show()
