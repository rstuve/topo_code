"""
July 5, 2022
Author: Ryan Stuve

Moves transverse energy data from root file to numpy array saved to file,
presents it as histogram using matplotlib.pyplot

uses makeHist() to create file 'npfile.npz', function can be exported (see hist_coe.py)
"""
from ROOT import TFile
import numpy as np
import matplotlib.pyplot as plt

def printProgress(event, numEntries):
    " If large number of events, used to show progress "
    checkpoint = numEntries // 100
    if event % checkpoint == 0:
        progress = int(event/checkpoint)
        print("Loading: [{:<10s}] {}% complete".format('▭'*int(progress / 10), progress), end='\r')

def makeHist(cycle='2',v=True,layer=1, numEntries = 0, progress = False):
    """ produces np histogram and saves it to file npfile.npz 
        v prints updates to stdout, progress shows progress bar """
    
    etaSet = 1.4 # max eta value
    etaGran = .125 # eta granularity
    phiSet = 3.1 # max phi
    phiGran = .1
    binSize = 50 # how many MeV per hist bin
    max = 1000 # max value of histogram

    if v:
        print('Preprocessing...')

    f = TFile('../data/user.bochen.25650990.OUTPUT._000001.root')
    tree = f.Get("SCntuple;"+cycle)
    if numEntries == 0: # unspecified number of events, use all
        numEntries = tree.GetEntries()

    Et = [] # array to store Et values
    for event in range(numEntries):
        tree.GetEntry(event)
        Ets = tree.scells_Et
        samples = tree.scells_sampling # gets layer information
        etas = (np.asarray(tree.scells_eta) + etaSet) // etaGran # indexes etas
        phis = (np.asarray(tree.scells_phi) + phiSet) // phiGran

        # Create list of tuples of form (eta, phi, Et), sorted by eta then phi
        l = [(tuple[1:]) for tuple in zip(samples,etas,phis,Ets) if tuple[0] == layer]
        l.sort()

        eta_i = 0
        phi_i = 0
        currentV = 0

        for tuple in l:
            if tuple[0] == eta_i: # if same eta
                if tuple[1] == phi_i: # if same phi
                    currentV += tuple[2] # in same location, added together
                else:
                    if currentV != 0:
                        Et.append(currentV)
                    phi_i = tuple[1] # move to next phi slice
                    currentV = tuple[2]
            elif 0 < tuple[0] <= int(etaSet*2//etaGran): # if eta in etaSet
                if currentV != 0:
                    Et.append(currentV)
                eta_i = tuple[0] # move to next eta and phi
                phi_i = tuple[1]
                currentV = tuple[2]

        if currentV != 0:
            Et.append(currentV) # append final value

        if progress:
            printProgress(event, numEntries)

    if v:
        print("Converting data...")
    if v:
        print("Data processed, creating histogram...")

    Et = np.asarray(Et)
    hist, bins = np.histogram(Et, bins = int(max/binSize), range=[0,max])

    b = (bins[:-1] + bins[1:])/2
    np.savez('../data/npfile.npz', hist)

    return hist, b

if __name__ == '__main__':  # shows histogram
    hist, b = makeHist()
    plt.plot(b,hist, ds = 'steps')
    plt.title("scells_Et_Cycle_"+cycle)
    plt.xlabel("Tranverse Energy (Mev)")
    plt.ylabel("Counts / {binSize} MeV")
    plt.show()
