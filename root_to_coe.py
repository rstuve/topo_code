"""
Ryan Stuve
Modified: 07/15/2022
Extracts ET data from .root file, moves into individual .coe files for each
layer per event with specified bit width, organized by eta and phi
Files stored in sibling directory named "data", must be created before run and
contain .root file

Number of event files can be changed in line 163
"""

## 1) IMPORTS ___________________________
from ROOT import TFile
import os, time
import numpy as np
### END Imports==============================================

## 2a) USER INPUTS _____________________________
bit_size = 10 # max size of .coe file entry
allowNegEts = False
threshold = False
etaSet = 1.4 # max eta value
etaGran = .125 # eta granularity
etaCount = etaSet*2//etaGran + 1 # number of eta slices, max index
phiSet = 3.1 # max phi
phiGran =.098
phiCount = phiSet*2//phiGran + 1 # number of phi slices, max index
coeLineLength = 128
thresholds = {0:180,1:30,2:140,3:30} # Averages eyeballed from noise_tot_plot_OFLCOND-MC12-HPS-19-200-25.pdf


layers = [0,1,2,3] # layers to process, ie: [0,1,2,3,4,5] does layers 0-5
filename = '../data/user.bochen.25650990.OUTPUT._000001.root'
cycle = "SCntuple;2"
Reason='To condense ET data from cycle into .coe files' # printed out in readme file

## 2b) FIND START TIME ________________________
time_format=str('%4d_%02d_%02d-%02d:%02d:%02d')
date_format = str('%4d_%02d_%02d')
time_start=time_format % time.localtime()[0:6]
date=date_format % time.localtime()[0:3]
print('start time :', time_start)

## 2c) SET DATA FILE/DIR ____________________________
file = TFile(filename)
tree = file.Get(cycle)
numOfEvents = tree.GetEntries() # loop over all events, can be changed on line 131
overflow_count = 0 # keeps track of ET values too large for .coe file
EXT='.coe'

## 2d) Create/Set Save-Directory Folder__________________
CurrentDir=os.getcwd()
dataDir = '/../data/'
pyScriptName=__file__
cutoff = len(CurrentDir)+1
pyScriptNameBase=pyScriptName[cutoff:-3] # Remove last 3 char, '.py'
newDir = CurrentDir+dataDir+pyScriptNameBase
dirfmt=str(newDir+'/%4d_%02d_%02d-h%02d-m%02d-s%02d_'+cycle)
SaveDirName = dirfmt % time.localtime()[0:6]
SaveDirName=SaveDirName+'/'
try:
    os.mkdir(newDir + '/') # creates directory with same name as script
except:
    pass # if directory already exists

try:
    os.mkdir(SaveDirName)
    print('Save-to directory is ',SaveDirName[-35:])
except OSError:
    print('save-to directory already exists')
    pass # already exists, shouldn't happen

## END User Settings  ==========================================================

def findMax():
    'returns cutoff value for .coe entries'
    binMax = 10**bit_size
    return int(str(binMax),2)

def modifyEt(Et):
    'Modifies and returns binary representations of decimal ET values'
    global overflow_count
    maxNum = findMax()
    # Can convert Et from Mev to Gev here: Et /= 1000
    if Et < 0:
        Et = 0 if allowNegEts else None # sets all negative values to 0, not tested
    elif threshold and Et < thresholds[layer]*2:
        Et = 0
    elif Et >= maxNum:
        Et = maxNum - 1 # changes overflow values to max binary value
        overflow_count += 1

    Et = '{0:0{1}b}'.format(int(Et),bit_size) # convert to binary of specified bit size

    return Et

def sumBin(bin1,bin2):
    'Sums two binary strings, returns the total as a binary string'
    total = int(bin1,2) + int(bin2,2)
    returnValue = '{0:0{1}b}'.format(total,bit_size)

    if len(returnValue) > bit_size:
        returnValue = '1'*bit_size # if value overflows bit size

    return returnValue

def showProgress(event):
    'visual progress bar during script runtime'
    checkpoint = 10#numOfEvents // 100
    if event % checkpoint == 0:
        progress = int(event/checkpoint)
        print("Creating files: [{:<10s}] {}% complete".format('???'*int(progress / 10), progress), end='\r')

#=== Main script =====================================================
if __name__ == "__main__":

    ###__Create Readme.txt file in savedir________________________________#
    ThisCode=os.path.basename(__file__) # get name of this script when it runs
    file_name='ReadMe.txt'
    path = os.path.join(SaveDirName, file_name)
    with open(path, 'w+') as stream:
        stream.write(('py script start time : '+ str(time_start)+'\r\n'+'\r\n'))
        stream.write(('Data File used : '+ filename+'\r\n'))
        stream.write(('eta granularity : '+ '{}'.format(etaGran)+'\r\n'))
        stream.write(('phi granularity : '+ '{}'.format(phiGran)+'\r\n'))
        stream.write(('units : MeV'+'\r\n'))
        stream.write(('The python script ran was :   '+ThisCode+'\r\n'))
        stream.write(('The purpose of this run was : '+Reason+'\r\n'))
        stream.write(('save to directory is '+SaveDirName+'\r\n'+'\r\n'))
        # adds script end time at bottom of code
    ###__End of Create/write Readme.txt File =================

    cycle_start=time_format % time.localtime()[0:6]
    print('loop start time :', cycle_start)

    for layer in layers:
        print()
        print(f'Processing layer {layer}')
        layerDir = SaveDirName + f"layer_{layer}/"
        os.mkdir(layerDir)

        f1 = open(layerDir + "file_1"+EXT, 'a') # create pointers to each file
        f2 = open(layerDir + "file_2"+EXT, 'a')
        f3 = open(layerDir + "file_3"+EXT, 'a')
        f4 = open(layerDir + "file_4"+EXT, 'a')
        f5 = open(layerDir + "file_5"+EXT, 'a')
        files = [f1,f2,f3,f4,f5] # store pointers in list to iterate over

#____ Write headers for each file ___________________
        i = 1
        for f in files:
            f.write(";InputFileName = {0}, wrote: {1}, \
Eta range: (-{2},{2}), step={3}, \
Phi range: (-{4},{4}), step={5},  \
bit length = {6}\n\
".format(f'layer_{layer}/file_{i}'+EXT, date, etaSet, etaGran, phiSet, phiGran,bit_size))

            f.write('memory_initialization_radix =2;\n')
            f.write('memory_initialization_vector =\n')
            i += 1

#_______ End header __________________________________
        for event in range(500):#numOfEvents): # Can be changed to reduce events processed
            showProgress(event)
            tree.GetEntry(event) # reduces tree to single event, changes for each iteration
            Ets=list(map(modifyEt, tree.scells_Et)) # apply modification to ET values
            samples = tree.scells_sampling
            etas = (np.asarray(tree.scells_eta) + etaSet) // etaGran # reduces etas to indices starting at 0
            phis = (np.asarray(tree.scells_phi) + phiSet) // phiGran # same as etas above

            # make a list of tuples with form (eta, phi, ET) for all ET data given in that layer
            l = [(tuple[1:]) for tuple in zip(samples,etas.copy(),phis.copy(),Ets.copy()) if tuple[0] == layer]
            l.sort() # sort by eta indices and then phi indices in order for loop to work
            eta_i = 0 # initialize indices at 0
            phi_i = 0
            currentV = '0'*bit_size # ET sum at current eta and phi, reset when either changes

            finalEt = '' # string that holds ET values, written to file at end of loop

            #loop through phi slices left to right, moving to next eta slice when done
            lines = []
            for tuple in l:
                if tuple[0] == eta_i: # if same eta
                    if tuple[1] == phi_i: # if same phi
                        currentV = sumBin(currentV, tuple[2]) # add ET to sum at that point

                    elif 0 <= tuple[1] < phiCount:
                        finalEt += currentV # write current ET to file
                        phi_i += 1 # move to next phi slice
                        while phi_i != tuple[1]:
                            if phi_i > phiCount:
                                print(prev_tuple)
                                print(event)
                                print(tuple)
                                print(phi_i)
                                print()
                                quit()
                            finalEt += '0'*bit_size # fill grid with 0s until another data value is reached
                            phi_i += 1
                        currentV = tuple[2] # set ET sum to new data value's ET

                elif 0 <= tuple[0] < etaCount: # if eta in specified eta range
                    if 0 <= tuple[1] < phiCount: # if phi in specified range
                        finalEt += currentV # write current ET to file
                        phi_i += 1 # move to next phi slice
                        finalEt += '0'*bit_size*int(phiCount-phi_i) # no more values in eta slice, finish line with 0s
                        lines.append(finalEt)
                        finalEt = ''
                        eta_i += 1 # move to next eta slice
                        while eta_i < etaCount and eta_i != tuple[0]:
                            finalEt += '0'*bit_size*int(phiCount) # fill lines with 0 until next data value reached
                            lines.append(finalEt)
                            finalEt = ''
                            eta_i += 1
                        phi_i = 0 # reset phi index to far left
                        while phi_i < phiCount and phi_i != tuple[1]:
                            finalEt += '0'*bit_size # fill with zeroes until first data point of new eta slice
                            phi_i += 1
                        currentV = tuple[2] # set ET sum to new data value's ET


            finalEt += currentV # write final ET sum to file
            phi_i += 1
            finalEt += '0'*bit_size*int(phiCount-phi_i) # fill line with 0s
            lines.append(finalEt)
            finalEt = ''
            eta_i += 1
            while eta_i < etaCount:
                finalEt += '0'*bit_size*int(phiCount) # fill all remaining lines with 0s
                lines.append(finalEt)
                finalEt = ''
                eta_i += 1

            for line in lines:
                for i in range(0, len(line), coeLineLength):
                    files[i//coeLineLength].write(line[i:i+coeLineLength]+'\n')

        for f in files:
            f.close()

#== finish process ====================================================
    cycle_end=time_format % time.localtime()[0:6]
    print('\nloop end time :', cycle_end)

    print('Done with files')
    print('overflow =',overflow_count) # print count of ET values that exceeded bit size
    time_end=time_format % time.localtime()[0:6]
    with open(path, 'a') as stream:
        stream.write(('\npy script end time : '+ str(time_end)+'\r\n'+'\r\n'))
    print('end time : ', time_end)
