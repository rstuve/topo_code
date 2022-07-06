"""
Author: Ryan Stuve
Date modified: 7/1/2022

Presents .coe file as visual histogram of energies
"""
import os
import numpy as np
import matplotlib.pyplot as plt
import atlas_mpl_style as ampl


# Get files and data
run_folder = '2022_07_05-h15-m37-s25_SCntuple;2'
layer = 1
bit_size = 10
numOfEvents = 1
currentDir = os.getcwd()
binSize = 50
max = 1000

npzfile = np.load('../data/npfile.npz')

Et = []
for event in range(1):#numOfEvents):
    lines = ''
    path = '../data/root_to_coe/' + run_folder + '/by_event/event_' + str(event) + '/'
    filename = 'Cell_EtsLayer'+str(layer)+'.coe'
    with open(path+filename) as f:
        for i in range(3):
            f.readline()
        for line in f.read().splitlines():
            lines += line

    EtT = [int(lines[i:i+bit_size], 2) for i in range(0, len(lines), bit_size)]
    for value in EtT:
        if value != 0:
            Et.append(value)

data = np.asarray(Et)
hist, bins = np.histogram(Et, bins = int(max/binSize), range=[0,max])
b = (bins[:-1] + bins[1:])/2

plt.figure(figsize = (12,8))
plt.plot(b,hist, ds = 'steps')
# root data
plt.plot(b,npzfile['arr_0'], ds = 'steps')

ampl.draw_atlas_label(0.7,0.95,simulation=1,energy="13 TeV",desc="scells_Et_Cycle_2, layer "+str(layer))#,lumi=139)
ampl.set_ylabel("Counts / 50 MeV")
ampl.set_xlabel("Tranverse Energy (Mev)")
plt.legend(['from .coe', 'from .root'])


plt.show()
