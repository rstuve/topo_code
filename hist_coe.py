"""
Author: Ryan Stuve
Date modified: 7/1/2022

Presents .coe file as visual histogram of energies, compared to .root histogram
"""
import numpy as np
import matplotlib.pyplot as plt
import atlas_mpl_style as ampl
from filtered_hist import makeHist


# Get files and data
run_folder = '2022_07_06-h13-m11-s28_SCntuple;2' # change to run folder
layer = 1 # which layer is being compared
numOfEvents = 1
max = 1000 # max value of ET
binSize = 50 # how big of bin in MeV


with open('../data/root_to_coe/' + run_folder + '/by_event/event_0/Cell_EtsLayer'+str(layer)+'.coe') as f:
    bit_size = int(f.readline()[137:]) # max size of Et in binary

# create root data for comparison
#makeHist(numEntries = numOfEvents, progress = True, layer = layer)
npzfile = np.load('../data/npfile.npz')

Et = []
for event in range(numOfEvents):
    lines = ''
    path = '../data/root_to_coe/' + run_folder + '/by_event/event_' + str(event) + '/'
    filename = 'Cell_EtsLayer'+str(layer)+'.coe'
    with open(path+filename) as f: # loop through files, storing ET values
        for i in range(3):
            f.readline()
        for line in f.read().splitlines():
            lines += line

    EtT = [int(lines[i:i+bit_size], 2) for i in range(0, len(lines), bit_size)]
    for value in EtT:
        if value != 0: # ignore 0 values
            Et.append(value)
            print(value)
        else:
            print(value)
    #print(len(Et))
quit()

data = np.asarray(Et)
hist, bins = np.histogram(Et, bins = int(max/binSize), range=[0,max])
b = (bins[:-1] + bins[1:])/2

plt.figure(figsize = (12,8))
plt.plot(b,hist, ds = 'steps')

plt.plot(b,npzfile['arr_0'], ds = 'steps') # root data

ampl.draw_atlas_label(0.7,0.95,simulation=1,energy="13 TeV",desc=f"scells_Et_Cycle_2, layer {layer}, up to {numOfEvents} events")#,lumi=139)
ampl.set_ylabel("Counts / 50 MeV")
ampl.set_xlabel("Tranverse Energy (Mev)")
plt.legend(['from .coe', 'from .root'])


plt.show()
