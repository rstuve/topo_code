##======================================
## Ryan Stuve
## Modified: 06/24/2022
## Extracts ET data from .root file, moves into individual .coe files for each
## event with specified bit width and organized by eta and phi
##======================================

## 1) IMPORTS ___________________________
import uproot
import os, time
import numpy as np
### END Imports==============================================

## 2) USER SETTINGS _________________________________________

## 2a) USER INPUTS _____________________________
bit_size = 10 # max size of .coe file entry
etaSet = 1.4 # max eta value
etaGran = .125 # eta granularity
phiSet = 3.1 # max phi
phiGran = .1
eta_dec = 3 # decimal places needed for eta value
sample = 1 # sample number that data is taken from
filename = '../data/user.bochen.25650990.OUTPUT._000001.root' # if changing files or cycles, ensure cycle still
cycle = "SCntuple;2"                                  # has ['scells_Et'] in directory
Reason='To condense ET data from cycle into .coe file'

## 2b) FIND START TIME ________________________
time_format=str('%4d_%02d_%02d-%02d:%02d:%02d')
time_start=time_format % time.localtime()[0:6]
print('start time :', time_start)

## 2c) SET DATA FILE/DIR ____________________________
datafile=uproot.open(filename)
datatree = datafile[cycle].arrays()
numOfEvents=len(datatree)
overflow_count = 0 # keeps track of ET values too large for .coe file
EXT='.coe'

## 2d) Create/Set Save Directory Folder__________________
CurrentDir=os.getcwd()
print('The current working directory is',CurrentDir)
dataDir = '../data/'
pyScriptName=__file__
cutoff = len(CurrentDir)+1
pyScriptNameBase=pyScriptName[cutoff:-3] # Remove last 3 char, '.py'
newDir = CurrentDir+dataDir+pyScriptNameBase
dirfmt=str(newDir+'/%4d_%02d_%02d-h%02d-m%02d-s%02d_'+cycle)
SaveDirName = dirfmt % time.localtime()[0:6]
SaveDirName=SaveDirName+'/'
SaveDirNameEvents = SaveDirName+'by_event/'
try:
    os.mkdir(pyScriptNameBase + '/') # creates directory with same name as script
except:
    pass # if directory already exists

try:
    os.mkdir(SaveDirName)
    os.mkdir(SaveDirNameEvents)
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
    # Convert Et from Mev to Gev: Et /= 1000
    if Et < 0:
        Et = None # throws out negative Et, not tested
    if Et >= maxNum:
        Et = '1'*bit_size
        overflow_count += 1 # changes overflow values to max bin
    else:
        Et = '{0:0{1}b}'.format(int(Et),bit_size)

    return Et

def sumBinList(binList):
    'Sums a list of binary strings, returns the total as a binary string'
    total = 0
    for bin in binList:
        total += int(bin,2)
    returnValue = '{0:0{1}b}'.format(total,bit_size)

    if len(returnValue) > bit_size:
        returnValue = '1'*bit_size # if value overflows bit size

    return returnValue

def showProgress(event):
    'visual progress bar during script runtime'
    checkpoint = numOfEvents // 100
    if event % checkpoint == 0:
        progress = int(event/checkpoint)
        print("Creating files: [{:<10s}] {}% complete".format('▭'*int(progress / 10), progress), end='\r')

#=======================================================================
if __name__ == "__main__":

    ###__Create Readme.txt file in savedir________________________________#
    ThisCode=os.path.basename(__file__) # get name of this script when it runs
    file_name='ReadMe'##+ SaveDirName[-23:]  # 22 last 19 char of SaveDirName[-19:]
    path = os.path.join(SaveDirName, file_name)
    with open(path, 'w+') as stream:
        stream.write(('py script start time : '+ str(time_start)+'\r\n'+'\r\n'))
        stream.write(('Data File used : '+ filename+'\r\n'))
        stream.write(('cycle used :     '+ cycle+'\r\n'+'\r\n'))
        stream.write(('The python script ran was :   '+ThisCode+'\r\n'))
        stream.write(('The purpose of this run was : '+Reason+'\r\n'))
        stream.write(('save to directory is '+SaveDirName+'\r\n'+'\r\n'))
        # adds script end time at bottom of code
    ###__End of Create/write Readme.txt File =================

    etaSlices = np.arange(-etaSet,etaSet,etaGran) # final eta layers
    phiSlices = np.arange(-phiSet,phiSet,phiGran) # final phi layers
    phiSlices = phiSlices.round(1)

    cycle_start=time_format % time.localtime()[0:6]
    print('loop start time :', cycle_start)

    for event in range(numOfEvents):
        showProgress(event)
        e = datatree[event]
        samples = np.asarray(e['scells_sampling'])
        indices = np.where(samples == sample)
        etaList = e['scells_eta'][indices]
        phiList = e['scells_phi'][indices]

        binMap=map(modifyEt, e['scells_Et']) # Modify values, convert to binary
        etList = np.array(list(binMap))[indices]


        finalEt = '' # Stores final grid of Et values back to back, new line for new eta slice
        for i in etaSlices:
            in_eta = (i<etaList) & (etaList<(i+etaGran))
            for j in phiSlices:
                et = etList[np.where(in_eta & (j<phiList) & (phiList<(j+phiGran)))]
                t = sumBinList(et)
                finalEt += t
            finalEt += '\n'
        with open(SaveDirNameEvents+'_input_data_event%s'% event + EXT, 'a') as f:
            f.write('memory_initialization_radix =2;\nmemory_initialization_vector =\n')
            f.write(finalEt)


    cycle_end=time_format % time.localtime()[0:6]
    print('\nloop end time :', cycle_end)

    print('Done with files')
    print('overflow =',overflow_count)
    time_end=time_format % time.localtime()[0:6]
    with open(path, 'a') as stream:
        stream.write(('\npy script end time : '+ str(time_end)+'\r\n'+'\r\n'))
    print('end time : ', time_end)
