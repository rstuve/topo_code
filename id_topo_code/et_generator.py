"""
July 25, 2022
Author: Ryan Stuve

Moves transverse energy data from root file to numpy array saved to file

uses makeList() to create et lists
"""
from ROOT import TFile
import numpy as np

def makeList(layer, cycle='2', start = 0, stop = 99, threshold = False):
    """ produces array list for given layer from start to stop (inclusive)"""

    binSize = 50 # how many MeV per hist bin
    max = 1000 # max value of histogram
    thresholds = {0:180,1:30,2:140,3:50}

    f = TFile('../data/user.bochen.25650990.OUTPUT._000001.root')
    tree = f.Get("SCntuple;"+cycle)
    etList = []
    for event in range(start,stop+1):
        tree.GetEntry(event)
        Ets = tree.scells_Et
        samples = tree.scells_sampling # gets layer information
        etas = tree.scells_eta

        [etList.append(tuple[2]) for tuple in zip(samples,etas,Ets) if tuple[0] == layer
         and -1.4 <= tuple[1] <= 1.402
         and (not threshold or tuple[2] >= thresholds[layer]*2)]

    etList = np.asarray(etList)
    return etList

if __name__ == '__main__':
    ets = []
    for i in range(4):
        ets.append(makeList(layer=i, start=0, stop=0,threshold=False))
    np.savez(f'../data/et_lists/events{start}-{stop}_no_thresh.npz',ets[0],ets[1],ets[2],ets[3])
