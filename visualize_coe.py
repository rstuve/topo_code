"""
Author: Ryan Stuve
Date modified: 7/15/2022

Presents .coe file as visual graph of energies
"""
import os
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import LogNorm

# Get file and data
run_folder = '2022_07_19-h12-m51-s45_SCntuple;2' # change based off location of event
numOfEvents = 1
layer = 0

currentDir = os.getcwd()
path = '../data/root_to_coe/' + run_folder + '/layer_' + str(layer) + '/'
f1 = open(path+"file_1.coe")
f2 = open(path+"file_2.coe")
f3 = open(path+"file_3.coe")
f4 = open(path+"file_4.coe")
f5 = open(path+"file_5.coe")
files = [f1,f2,f3,f4,f5]

#== parsing info, should match file headers ===============
bit_size = 10
etaSet = 1.4
etaGran = .125
phiSet = 3.1
phiGran = .098

etaCount = int(etaSet*2//etaGran + 1)

for i in range(3): # skip header
    for file in files:
        file.readline()


# combine files into one list of strings of ET values
lines = []
for i in range(etaCount*numOfEvents):
    for file in files:
        try:
            lines[i] += file.readline().strip()
        except:
            lines.append(file.readline().strip())

for file in files:
    file.close()

# Move data into np.array
Ets = np.empty((0,int(len(lines[0])/bit_size)))

for line in lines[:etaCount]: # first event
    EtT = [int(line[i:i+bit_size], 2) for i in range(0, len(line), bit_size)]
    Ets = np.append(Ets, np.array([EtT]), axis=0)

'''
j = 0
for line in lines[etaCount:]: # sum up ET from all events
    EtT = [int(line[i:i+bit_size], 2) for i in range(0, len(line), bit_size)]
    Ets[j % etaCount] += EtT
    j += 1
'''

if not np.any(Ets): # if there are no values besides 0s
    raise ValueError("plot requires at least 1 Et value")

print(np.count_nonzero(Ets))

#== Plot np.array =================
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(np.rot90(Ets), norm = LogNorm(),extent=[-etaSet,etaSet,-phiSet,phiSet])
plt.xlabel('$\eta$')
plt.ylabel('$\phi$')
plt.title("Events 0-"+str(numOfEvents)+', Layer '+str(layer),y = 1.05, fontweight="bold")
plt.tick_params(bottom=True, top=False, left=True, right=False,
labelbottom=True, labeltop=False, labelleft=True,labelright=False)
cb = fig.colorbar(cax)
cb.set_label('MeV', rotation = 0, loc = 'bottom')

plt.show()
