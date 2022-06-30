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
EtaSet = 2.4
eta_dec = 3 # decimal places needed for eta value
filename = 'user.bochen.25650990.OUTPUT._000001.root' # if changing files or layers, ensure layer still
layer = "SCntuple;"+input("Which layer?\n> ")         # has ['scells_Et'] in directory
Reason='To condense ET data from layer into .coe file'

## 2b) FIND START TIME ________________________
time_format=str('%4d_%02d_%02d-%02d:%02d:%02d')
time_start=time_format % time.localtime()[0:6]
print('start time :', time_start)

## 2c) SET DATA FILE/DIR ____________________________
datafile=uproot.open(filename)
datatree = datafile[layer].arrays()
NumOfEvents=len(datatree)
overflow_count = 0 # keeps track of ET values too large for .coe file
EXT='.coe'

## 2d) Create/Set Save Directory Folder__________________
CurrentDir=os.getcwd()
print('The current working directory is',CurrentDir)
pyScriptName=__file__
pyScriptNameBase=pyScriptName[:-3] # Remove last 3 char, '.py'
dirfmt=str(pyScriptNameBase+'/%4d_%02d_%02d-h%02d-m%02d-s%02d_'+layer)
SaveDirName = dirfmt % time.localtime()[0:6]
SaveDirName=SaveDirName+'/'
SaveDirNameEtaValues=SaveDirName+'by_eta_values/'
#SaveDirNameEtaSlices=SaveDirName+'by_eta_Slices/'
#SaveDirNameEtValues=SaveDirName+'Et_values/'
try:
    os.mkdir(pyScriptNameBase + '/')
except:
    pass # if directory already exists

try:
    os.mkdir(SaveDirName)
    os.mkdir(SaveDirNameEtaValues)
    #os.mkdir(SaveDirNameEtaSlices)
    #os.mkdir(SaveDirNameEtValues)
    print('Save-to directory is ',SaveDirName)
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
        Et = None
        overflow_count += 1
    else:
        Et = '{0:0{1}b}'.format(int(Et),bit_size)

    return Et

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
        stream.write(('Layer used :     '+ layer+'\r\n'+'\r\n'))
        stream.write(('The python script ran was :   '+ThisCode+'\r\n'))
        stream.write(('The purpose of this run was : '+Reason+'\r\n'))
        stream.write(('save to directory is '+SaveDirName+'\r\n'+'\r\n'))
        # adds script end time at bottom of code
    ###__End of Create/write Readme.txt File =================

    ### Create lists of eta and phi values:
    event0 = datatree[0]
    Eta = event0['scells_eta']
    phi = event0['scells_phi']

    EtaList=[]
    EtaFile00NameDict={}
    EtaDataSlicesDict={}
    EtaFile00NameDictReset={}

    n = 0
    for eta in Eta:
        if -EtaSet<=eta<=EtaSet:
            eta=round(eta,eta_dec)
            if eta not in EtaList:
                EtaList.append(eta)
                EtaFile00NameDict[str(eta)]="{:0>3}".format(n) # generate eta##.coe number name for slcie files
                EtaDataSlicesDict[str(eta)]=""
                n+=1

    for EtaValue in EtaList:
        with open(SaveDirNameEtaValues+layer+'_input_data_eta%s'% str(EtaValue)+EXT, 'a+') as f:
            f.write('memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =\r\n')

        #with open(SaveDirNameEtaSlices+LayerType+'_input_data_eta%s'% EtaFile00NameDict[str(EtaValue)]+EXT, 'a') as f:
        #    f.write('memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =\r\n')

        #with open(SaveDirNameEtaSlices+LayerType+'Sorted_input_data_eta%s'% EtaFile00NameDict[str(EtaValue)]+EXT, 'a') as f:
        #    f.write('memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =\r\n')



    #### Get et values........
    for event in range(1): #NumOfEvents):
        print(event)
        #showProgress(event)
        eventdata = datatree[event] # get data for event number
        EtT = eventdata['scells_Et']
        towers_in_event = len(EtT)
        Et = np.array(EtT,dtype=int)/10 ## MeV to .1 GeV, all Et at once

        binMap=map(modifyEt, Et) # Modify values, convert to binary
        Etbin = list(binMap)

        for tower in range(towers_in_event):
            EtaValue=round(Eta[tower], eta_dec)
            if EtaValue in EtaList:
                print('yay')
                et= Etbin[tower]
                with open(SaveDirNameEtaValues+layer+'_input_data_eta%s'%str(EtaValue) + EXT, 'a') as f: #
                    f.write(str(et))
            #with open(SaveDirNameEtaSlices+LayerType+'_input_data_eta%s'% EtaSliceDict[str(EtaValue)]+EXT, 'a') as f: #
            #    f.write(str(et))

        # write values to new .coe file
        #with open(SaveDirNameEtValues+'_input_data_et_event%s'% event+EXT, 'a+') as f:
        #        for Et in Etbin:
        #            if Et != None:
        #                f.write(Et+'\r\n')

    print('\nAll files complete.')
    print('overflow =',overflow_count)
    time_end=time_format % time.localtime()[0:6]
    with open(path, 'a') as stream:
        stream.write(('\npy script end time : '+ str(time_end)+'\r\n'+'\r\n'))
    print('end time : ', time_end)
