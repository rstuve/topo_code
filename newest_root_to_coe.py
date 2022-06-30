#!/usr/bin/python
##======================================
## Ryan Stuve
## Modified: 06/24/2022
## Extracts ET data from .root file, moves into individual .coe files for each event
##======================================

## 1) IMPORTS ___________________________
import uproot
import os, time
import numpy as np
### END Imports==============================================

## 2) USER SETTINGS _________________________________________

## 2a) USER INPUTS _____________________________
bit_size = 10 # max size of .coe file entry
etaSet = 1.4
etaGran = .125
phiSet = 3.1
phiGran = .1
eta_dec = 3 # decimal places needed for eta value
sample = 1
filename = 'user.bochen.25650990.OUTPUT._000001.root' # if changing files or cycles, ensure cycle still
cycle = "SCntuple;"+input("Which cycle?\n> ")         # has ['scells_Et'] in directory
Reason='To condense ET data from cycle into .coe file'

## 2b) FIND START TIME ________________________
time_format=str('%4d_%02d_%02d-%02d:%02d:%02d')
time_start=time_format % time.localtime()[0:6]
print('start time :', time_start)

## 2c) SET DATA FILE/DIR ____________________________
datafile=uproot.open(filename)
datatree = datafile[cycle].arrays()
NumOfEvents=len(datatree)
overflow_count = 0 # keeps track of ET values too large for .coe file
EXT='.coe'

## 2d) Create/Set Save Directory Folder__________________
CurrentDir=os.getcwd()
print('The current working directory is',CurrentDir)
pyScriptName=__file__
pyScriptNameBase=pyScriptName[:-3] # Remove last 3 char, '.py'
dirfmt=str(pyScriptNameBase+'/%4d_%02d_%02d-h%02d-m%02d-s%02d_'+cycle)
SaveDirName = dirfmt % time.localtime()[0:6]
SaveDirName=SaveDirName+'/'
SaveDirNameEtaValues = SaveDirName+'by_eta_values/'
try:
    os.mkdir(pyScriptNameBase + '/')
except:
    pass # if directory already exists

try:
    os.mkdir(SaveDirName)
    os.mkdir(SaveDirNameEtaValues)
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
    if Et < 0:
        Et = None
    if Et >= maxNum:
        Et = '1'*bit_size
        overflow_count += 1
    else:
        Et = '{0:0{1}b}'.format(int(Et),bit_size)

    return Et

def filterEta(eta):
    global excluded_etas
    if -etaSet<=eta<=etaSet:
        eta = round(eta, eta_dec)
    else:
        excluded_etas += 1
        eta = None
    return eta

def showProgress(event):
    'visual progress bar during script runtime'
    checkpoint = NumOfEvents // 100
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

    ### Create lists of eta and phi values:
    excluded_etas = 0
    etaEtList = []

    cycle_start=time_format % time.localtime()[0:6]
    print('loop start time :', cycle_start)

    for event in range(1):
        showProgress(event)
        e = datatree[event]
        samples = e['scells_sampling']
        EtaT = e['scells_eta']
        EtT = e['scells_Et']
        phi = e['scells_phi']
        Ets_in_event = len(EtT)

        Et = np.array(EtT,dtype=int)#/1000 ## MeV to GeV, all Et at once
        binMap=map(modifyEt, Et) # Modify values, convert to binary
        Etbin = list(binMap)

        tempEta = np.array(EtaT,dtype=float)
        etaMap = map(filterEta, tempEta)
        Eta = list(etaMap)

        z = zip(samples,Eta,phi,Etbin)
        etaEtList += [(eta,phi,et) for sp,eta,phi,et in z if sp == sample and eta != None]

    cycle_end=time_format % time.localtime()[0:6]
    print('loop end time :', cycle_end)
    print('Writing files: ')

    etaEtList.sort()
    etaSlices = np.arange(-etaSet,etaSet,etaGran)
    phiSlices = np.arange(-phiSet,phiSet,phiGran)





    for m in range(5):
        print(str(etaEtList[m])+': {},{},{}'.format(etas[m],phis[m],ets[m]))
#    prev_eta = -etaSet - 1 # must be lower than first element
#    for tuple in etaEtList[:10]:
#        Eta, Et = tuple
#        print(Eta)
#        if Eta == prev_eta:
#            f.write(Et)
#        else:
#            if prev_eta != -etaSet - 1:
#                f.close()
#                print(prev_eta,Eta)
#            f = open(SaveDirNameEtaValues+'_input_data_eta%s'% Eta+EXT, 'a')
#            f.write('memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =\r\n')
#            f.write(Et)
#            Eta = prev_eta
#    f.close()

    print('Done with files')
    print('overflow =',overflow_count)
    print(f'{excluded_etas} etas were excluded')
    time_end=time_format % time.localtime()[0:6]
    with open(path, 'a') as stream:
        stream.write(('\npy script end time : '+ str(time_end)+'\r\n'+'\r\n'))
    print('end time : ', time_end)
