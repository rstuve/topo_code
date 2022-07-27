"""
July 25, 2022
Author: Ryan Stuve

Moves transverse energy data from root file to numpy array saved to file,
presents it as histogram using matplotlib.pyplot

uses makeHist() to create file 'npfile.npz', function can be exported (see hist_coe.py)
"""
from ROOT import TFile
import numpy as np
import matplotlib.pyplot as plt

def makeHist(cycle='2',layer=1, numEntries = 0, threshold = False):
    """ produces np histogram """

    binSize = 50 # how many MeV per hist bin
    max = 1000 # max value of histogram
    thresholds = {0:180,1:30,2:140,3:50}

    f = TFile('../data/user.bochen.25650990.OUTPUT._000001.root')
    tree = f.Get("SCntuple;"+cycle)
    if numEntries == 0: # unspecified number of events, use all
        numEntries = tree.GetEntries()
    etList = []
    for event in range(numEntries):
        tree.GetEntry(event)
        Ets = tree.scells_Et
        samples = tree.scells_sampling # gets layer information
        etas = tree.scells_eta

        [etList.append(tuple[2]) for tuple in zip(samples,etas,Ets) if tuple[0] == layer
         and -1.3989652395248413 <= tuple[1] <= 1.4014792442321777
         and (not threshold or tuple[2] >= thresholds[layer]*2)]

    etList = np.asarray(etList)
    hist, bins = np.histogram(etList, bins = int(max/binSize), range=[0,max])

    b = (bins[:-1] + bins[1:])/2
    return hist, b

if __name__ == '__main__':  # shows histogram

    hist, b = makeHist()
    plt.plot(b,hist, ds = 'steps')
    plt.title("scells_Et_Cycle_"+cycle)
    plt.xlabel("Tranverse Energy (Mev)")
    plt.ylabel("Counts / {binSize} MeV")
    plt.show()
