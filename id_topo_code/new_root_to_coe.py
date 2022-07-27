"""
Ryan Stuve
Modified: 07/27/2022
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
from funcMap import makeMap
### END Imports==============================================

## 2a) USER INPUTS _____________________________
bit_size = 10 # max size of .coe file entry
allowNegEts = False
threshold = True
corners = True
numOfEvents = 100

etaSet = 1.4 # max eta value
phiSet = 3.14159 # max phi
coeLineLength = 128
thresholds = {0:180,1:30,2:140,3:50} # Averages eyeballed from noise_tot_plot_OFLCOND-MC12-HPS-19-200-25.pdf
Granularities = {0: (0.02500000037252903, 0.09817477315664291),
                 1: (0.0031250000465661287, 0.09817477315664291), # taken from caloCellsMap file
                 2: (0.02500000037252903, 0.02454369328916073),
                 3: (0.05000000074505806, 0.02454369328916073) }
cornerValues = {0:800,1:900,2:910,3:920}

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
    maxNum = findMax()
    # Can convert Et from Mev to Gev here: Et /= 1000
    if Et < 0:
        Et = 0 if allowNegEts else None # sets all negative values to 0, not tested
    elif threshold and Et < thresholds[layer]*2:
        Et = 0
    elif Et >= maxNum:
        Et = maxNum - 1 # changes overflow values to max binary value

    Et = '{0:0{1}b}'.format(int(Et),bit_size) # convert to binary of specified bit size

    return Et

def showProgress(event):
    'visual progress bar during script runtime'
    checkpoint = 1#numOfEvents // 100
    if event % checkpoint == 0:
        progress = int(event/checkpoint)
        print("Creating files: [{:<10s}] {}% complete".format('▭'*int(progress / 10), progress), end='\r')


#=== Main script =====================================================
if __name__ == "__main__":
    ThisCode=os.path.basename(__file__) # get name of this script when it runs

    for layer in layers:
        print()
        print(f'Processing layer {layer}')
        layerDir = SaveDirName + f"layer_{layer}/"
        os.mkdir(layerDir)

# _____import data from CaloCellsMap file _____
        grid, ls = makeMap(layer)
        idGrid = np.asarray(grid)

        with open(layerDir+'idGrid.txt', 'w') as gridFile:
            for line in idGrid:
                lineString = ' '.join([str(id) for id in line]) # create one long line for each eta slice
                gridFile.write(lineString+'\n')

        mainIDs, mainEtas, mainPhis = zip(*ls)
        mainEtas = np.array(mainEtas)

        etaGran, phiGran = Granularities[layer]
        phiCount = len(grid[0]) # number of phi slices
# _____________________________________________


###__Create Readme.txt file per layer________________________________#
        file_name='ReadMe.txt'
        path = os.path.join(layerDir, file_name)
        with open(path, 'w') as stream:
            stream.write(('The python script ran was :   '+ThisCode+'\n'))
            stream.write(('The purpose of this run was : '+Reason+'\n'))
            stream.write(('Data File used : '+ filename+'\n'))
            stream.write(('save to directory is '+SaveDirName+'\n\n'))
            stream.write(('Layer : {}'.format(layer)+'\n'))
            stream.write(('eta granularity : '+ str(etaGran)+'\n'))
            stream.write(('phi granularity : '+ str(phiGran)+'\n'))
            stream.write(('units : MeV'+'\n\n'))
            stream.write(('Number of events: '+str(numOfEvents)+'\n\n'))
            stream.write(('py script start time : '+ str(time_start)+'\n'))
            # adds script end time at bottom of code
###__End of Create/write Readme.txt File =================

        files = [] # store pointers in list to iterate over
        for i in range(int(bit_size*phiCount/coeLineLength)):
            files.append(open(layerDir + f"file_{i}"+EXT, 'a')) # stores pointer to file

#____ Write headers for each file ___________________
        i = 0
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
        for event in range(numOfEvents):
            showProgress(event)
            etGrid = np.full((len(grid),phiCount), '0000000000', dtype='<U10')
            if corners:
                etGrid[0,0] = '{0:0{1}b}'.format(cornerValues[layer],bit_size)
                etGrid[0,-1] = '{0:0{1}b}'.format(cornerValues[layer]+1,bit_size)
                etGrid[-1,0] = '{0:0{1}b}'.format(cornerValues[layer]+2,bit_size)
                etGrid[-1,-1] = '{0:0{1}b}'.format(cornerValues[layer]+3,bit_size)
            tree.GetEntry(event) # reduces tree to single event, changes for each iteration
            Ets=list(map(modifyEt, tree.scells_Et)) # apply modification to ET values
            samples = tree.scells_sampling
            etas = tree.scells_eta
            phis = tree.scells_phi

            # make a list of tuples with form (eta, ET) for all ET data given in that layer
            l = [(tuple[1:]) for tuple in zip(samples,etas,phis, Ets) if tuple[0] == layer]

            for entry in l:
                etaIndexes = np.where(mainEtas == entry[0])[0] # all indices matching entry's eta
                if len(etaIndexes) > 1: # if more than one matching eta
                    for i in etaIndexes:
                        if mainPhis[i] == entry[1]:
                            idloc = np.where(idGrid == mainIDs[i]) # find location of matching eta
                            if idloc[0].size > 0: # if on the grid
                                loc = (idloc[0][0],idloc[1][0]) # get grid location
                                if etGrid[loc] == '0000000000': # don't overwrite corners
                                    etGrid[loc] = entry[2] # store value in location
                            break

                else:
                    idloc = np.where(idGrid == mainIDs[etaIndexes[0]]) # find location of matching eta
                    if idloc[0].size > 0: # if match on grid
                        loc = (idloc[0][0],idloc[1][0]) # find grid location
                        if etGrid[loc] == '0000000000': # don't overwrite corners
                            etGrid[loc] = entry[2] # store value in location

            for line in etGrid:
                lineString = ''.join(line) # create one long line for each eta slice
                for i in range(0, len(lineString), coeLineLength): # cut line into chunks
                    files[i//coeLineLength].write(lineString[i:i+coeLineLength]+'\n')


        for f in files:
            f.close()

#== finish process ====================================================

    print('Done with files')
    time_end=time_format % time.localtime()[0:6]
    for layer in layers:
        with open(os.path.join(SaveDirName + f"layer_{layer}/ReadMe.txt"), 'a') as stream:
            stream.write(('npy script end time : '+ str(time_end)))
    print('end time : ', time_end)
