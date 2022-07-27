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
run_folder = '100_thresh_c' # change based off location of event
event = 0
layer = 3
numFiles = {0:5,1:5,2:20,3:20}
Granularities = {0: (0.02500000037252903, 0.09817477315664291),
                 1: (0.0031250000465661287, 0.09817477315664291), # taken from caloCellsMap file
                 2: (0.02500000037252903, 0.02454369328916073),
                 3: (0.05000000074505806, 0.02454369328916073) }

currentDir = os.getcwd()
path = '../data/new_root_to_coe/' + run_folder + '/layer_' + str(layer) + '/'
files = []
for i in range(numFiles[layer]):
    files.append(open(path+f'file_{i}.coe', 'r'))

#== parsing info, should match file headers ===============
bit_size = 10
etaSet = 1.405
etaGran, phiGran = Granularities[layer]
phiSet = 3.1416


for i in range(3): # skip header
    for file in files:
        file.readline()

# combine files into one list of strings of ET values
lines = []
lines.append(files[0].readline().strip())
for file in files[1:]:
    lines[0] += file.readline().strip()

i=1
line = '1'*bit_size
while line[:bit_size] != lines[0][:bit_size]:
    line = files[0].readline().strip()
    lines.append(line)
    for file in files[1:]:
        lines[i] += file.readline().strip()
    i += 1
eventLength = i-1
'''
for i in range(eventLength*(event-1)):
    for file in files:
        file.readline()
i = 1
while files[0].readline():
    i += 1
print(i)
quit()
'''
for i in range(eventLength*event-1):
    lines.append(files[0].readline().strip())
    for file in files[1:]:
        #if i == 11087:
        #    print(file.readline().strip())
        #    continue
        lines[i+eventLength+1] += file.readline().strip()
for file in files:
    file.close()

# Move data into np.array
Ets = np.empty((0,int(len(lines[0])/bit_size)))

for line in lines[eventLength*event:eventLength*(event+1)]:
    EtT = [int(line[i:i+bit_size], 2) for i in range(0, len(line), bit_size)]
    Ets = np.append(Ets, np.array([EtT]), axis=0)

if not np.any(Ets): # if there are no values besides 0s
    raise ValueError("plot requires at least 1 Et value")

print(np.count_nonzero(Ets))

#== Plot np.array =================
fig = plt.figure()
ax = fig.add_subplot(111)
cax = ax.matshow(np.rot90(Ets), norm = LogNorm(),extent=[-etaSet,etaSet,-phiSet,phiSet])
plt.xlabel('$\eta$')
plt.ylabel('$\phi$')
plt.title("Event "+str(event)+', Layer '+str(layer),y = 1.05, fontweight="bold")
plt.tick_params(bottom=True, top=False, left=True, right=False,
labelbottom=True, labeltop=False, labelleft=True,labelright=False)
cb = fig.colorbar(cax)
cb.set_label('MeV', rotation = 0, loc = 'bottom')

plt.show()
