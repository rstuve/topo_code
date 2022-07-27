"""
Author: Ryan Stuve
Date modified: 7/25/2022

Presents .coe file as visual histogram of energies, compared to .root histogram
"""
import numpy as np
import os
import matplotlib.pyplot as plt
import atlas_mpl_style as ampl
from new_filtered_hist import makeHist


# Get files and data
run_folder = '2022_07_27-h11-m11-s42_SCntuple;2' # change to run folder
layers = [0,1,2,3] # which layer is being compared
numOfEvents = 100
threshold = True
max = 1000 # max value of ET
binSize = 50 # how big of bin in MeV
bit_size = 10 # max size of Et in binary
numFiles = {0:5,1:5,2:20,3:20}

# create root data for comparison
unedited_hists = []
for layer in layers:
    hist, b = makeHist(numEntries = numOfEvents, layer = layer, threshold = threshold)
    unedited_hists.append(hist)

# get edited .coe data
currentDir = os.getcwd()
Ets_per_layer = []

for layer in layers:
    files = []
    path = '../data/new_root_to_coe/' + run_folder + '/layer_' + str(layer) + '/'
    for i in range(numFiles[layer]):
        files.append(open(path+f'file_{i}.coe', 'r'))

    for i in range(3): # skip header
        for file in files:
            file.readline()


    # combine files into one list of strings of ET values
    lines = []
    Ets = []

    i = 0
    for line in files[0].readlines():
        lines.append(line.strip())
        i += 1

    for file in files[1:]:
        i = 0
        for line in file.readlines():
            lines[i] = lines[i] + line.strip()
            i += 1

    for file in files:
        file.close()

    linesPerEvent = len(lines)/numOfEvents
    for i in range(len(lines)):
        EtT = [int(lines[i][j:j+bit_size], 2) for j in range(0, len(lines[i]), bit_size)]
        if i%linesPerEvent == 0 or i%linesPerEvent == linesPerEvent-1:
            EtT.pop(0)
            EtT.pop()
        for value in EtT:
            if value != 0: # ignore 0 values
                Ets.append(value)
    Ets_per_layer.append(np.asarray(Ets))

edited_hists = []
for layer_data in Ets_per_layer:
    hist, bins = np.histogram(layer_data, bins = int(max/binSize), range=[0,max])
    edited_hists.append(hist)

differences = []
for i in range(len(layers)):
    differences.append(edited_hists[i]-unedited_hists[i])


b = (bins[:-1] + bins[1:])/2

# Plot histograms
fig, axs = plt.subplots(2, len(layers), gridspec_kw={'height_ratios': [4, 1]})
fig.set_size_inches(12, 7)
fig.suptitle('Comparing .coe to root data')

if len(layers) > 1:
    for i in range(len(layers)):
        axs[0,i].set_title('Layer_{}'.format(i))
        axs[0,i].plot(b,edited_hists[i], ds = 'steps')
        axs[0,i].plot(b, unedited_hists[i], ds = 'steps') # root data
        if i != 0:
            axs[0,i].sharey(axs[0,0])
            axs[1,i].sharey(axs[1,0])

        axs[1,i].plot(b, differences[i], ds = 'steps', color='red')
        axs[1,i].sharex(axs[0,i])
    axs[0,len(layers)-1].legend(['.coe','.root'])

else:
    axs[0].plot(b, edited_hists[0], ds = 'steps')
    axs[0].plot(b, unedited_hists[0], ds = 'steps') # root data
    axs[1].plot(b, differences[i], ds = 'steps', color='red')
    axs[1].sharex(axs[0])
    axs[0].legend(['.coe','.root'])

for ax in plt.gcf().axes:
    ax.label_outer()

fig.text(0.5, 0.04, 'Transverse Energy (MeV)', ha='center', va='center')
fig.text(0.06, 0.5, 'Counts / 50 MeV', ha='center', va='center', rotation='vertical')
fig.text(0.06, 0.24, 'Differences:', ha='center', va='center', size = 'large')


#ampl.draw_atlas_label(0.7,0.95,simulation=1,energy="13 TeV",desc=f"scells_Et_Cycle_2, layer {layer}, up to {numOfEvents} events")#,lumi=139)
#ampl.set_ylabel("Counts / 50 MeV")
#ampl.set_xlabel("Tranverse Energy (Mev)")
#plt.legend(['from .coe', 'from .root'])


plt.show()
