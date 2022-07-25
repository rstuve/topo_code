"""
Author: Ryan Stuve
Date modified: 7/1/2022

Presents .coe file as visual histogram of energies, compared to .root histogram
"""
import numpy as np
import os
import matplotlib.pyplot as plt
import atlas_mpl_style as ampl
from filtered_hist import makeHist


# Get files and data
run_folder = '2022_07_19-h13-m07-s49_SCntuple;2' # change to run folder
layers = [0,1,2,3] # which layer is being compared
numOfEvents = 10
max = 1000 # max value of ET
binSize = 50 # how big of bin in MeV
bit_size = 10 # max size of Et in binary
etaCount = 23 # how many eta slices per event

# create root data for comparison
unedited_hists = []
for layer in layers:
    print(f"Layer {layer}:")
    hist, b = makeHist(numEntries = numOfEvents, progress = False, layer = layer, threshold = True)
    unedited_hists.append(hist)

# get edited .coe data
currentDir = os.getcwd()
Ets_per_layer = []

for layer in layers:
    path = '../data/root_to_coe/' + run_folder + '/layer_' + str(layer) + '/'
    f1 = open(path+"file_1.coe")
    f2 = open(path+"file_2.coe")
    f3 = open(path+"file_3.coe")
    f4 = open(path+"file_4.coe")
    f5 = open(path+"file_5.coe")
    files = [f1,f2,f3,f4,f5]

    for i in range(3): # skip header
        for file in files:
            file.readline()


    # combine files into one list of strings of ET values
    lines = []
    Ets = []

    for i in range(etaCount*numOfEvents):
        for file in files:
            try:
                lines[i] += file.readline().strip()
            except:
                lines.append(file.readline().strip())

    for file in files:
        file.close()

    for line in lines:
        EtT = [int(line[i:i+bit_size], 2) for i in range(0, len(line), bit_size)]
        for value in EtT:
            if value != 0: # ignore 0 values
                Ets.append(value)
    #print(len(Et))
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
