##======================================
## Testing numpy binary stuff, sorting and eta slicing
## 2017 03 02 mhd
#  leading bit: 0 if pos, 1 if neg
##======================================
# this file: Root-2-FPGA-spcll_v005.py

#   updated ___________________________________________
#   2017 03 02  :   def leadingBitn(my_int): method
#   2017 03 01  :   Mev -> Gev  Et/1000
#               :   23 -> 13 bit Et values
# _____________________________________________________

#   Check:  is numpy still needed
#           prior to using binnary Et Array
#           will remove or comment out leadingbit and build binary
#           to try and slice binnnary Et array in Root-2-FPGA-spcll_v005
# for jTowers previous version:
# 1.sort_test_sat_01.py ran over event 0 ok, wrote fpga_input##.coe files correct format
#   . no eta,phi sorting done in this version
# 2. next Renamed to: loop over 1024 events
# wed night 16 nov 2016 : added section to sort by phi then eta, not sorting did not match orig. root event plots.
#                       : this looks to be working correct, check bin(Et)-->Dec(Et) plots
# 2017 02 22  v002 change data dir at office mhd dell

## 1) IMPORTS ___________________________
from ROOT import *
from operator import itemgetter # for sort
import array
import inspect # also needed for lineno
import os, time # for os.getcwd() to find current DIR, and time for pause->time.sleep(1)#1sec pause
import math # for rounding of eta to force nice etas

import numpy as np
### END Imports==============================================

## 2) USER SETTINGS _____________________________
bit_size = 10
NumOfEvents=10000
EtaSet=1.4
CreateDir='y' # makes dir to save output to
TestPrint = 'n'
time_format2=str('/%4d_%02d_%02d-%02d:%02d:%02d')
time_start=time_format2 % time.localtime()[0:6]
print('start time : ', time_start)

user=os.getenv("HOME") #os.path.expanduser('~') # 'mhd' # move to top # can I read user home dir name to set this value ? do it later
print('user is :', user)

## 2b) SET DATA FILE/DIR ____________________________
datafile=TFile("user.bochen.25650990.OUTPUT._000001.root")
datatree = datafile.Get("SCntuple;2")
# End Set Data input file =========================================
##_ Create/Set Save Directory Folder__________________
if CreateDir=='y':
    CurrentDir=os.getcwd() # print 'The Current working Directory is ',CurrentDir ## #dirfmt = "/root/%4d-%02d-%02d %02d:%02d:%02d" ## #dirfmt = "/%4d_%02d_%02d %02d-%02d-%02d"
    pyScriptName=__file__
    pyScriptNameBase=pyScriptName[:-3] # Remove last 3 char, '.py'
    dirfmt=str(pyScriptNameBase+'/%4d_%02d_%02d-h%02d-m%02d-s%02d') #dirfmt=str(CurrentDir+'/%4d_%02d_%02d-%02d-%02d-%02d')
    SaveDirName = dirfmt % time.localtime()[0:6]
    SaveDirName=SaveDirName+'/' #SaveDirName = 'Test_Dir'
    SaveDirNameEtaValues=SaveDirName+'by_eta_values/'
    SaveDirNameEtaSlices=SaveDirName+'by_eta_Slices/'
    SaveDirNameChkTriplets=SaveDirName+'Usual_Triplets_for_chk/'
    try:
        os.mkdir(pyScriptNameBase + '/')
    except:
        pass # if directory already exists

    try:
        os.mkdir(SaveDirName)
        os.mkdir(SaveDirNameEtaValues)
        os.mkdir(SaveDirNameEtaSlices)
        os.mkdir(SaveDirNameChkTriplets)
    except OSError:
        print('save-to directory already exists')
        pass # already exists

    ###_ END :Create/Set Save Directory Folder=====================

## END User Settings  ==========================================================


## 3) FUNCTIONS defs __________________________
def findMax():
    'returns cutoff value for .coe entries'
    binMax = 10**bit_size
    return int(str(binMax),2)

def modifyEt(Et):
    'Modifies and returns binary representations of decimal ET values'
    maxNum = findMax()
    if Et < 0:
        Et = None
    if Et >= maxNum:
        Et = '1'*bit_size
    else:
        Et = '{0:0{1}b}'.format(int(Et),bit_size)

    return Et

def filterEta(eta):
    if -EtaSet<=eta<=EtaSet:
        eta = round(eta, eta_dec)
    else:
        eta = None
    return eta
##__ End : of Declare functions ================================================

TowerMode='sc'

if TowerMode=='sc':
    eta_dec=3 # scells need 3 decimal palces for eta
    datatree.SetBranchStatus('*', 0)
    datatree.SetBranchStatus('scells_Et', 1)
    datatree.SetBranchStatus('scells_eta', 1)
    datatree.SetBranchStatus('scells_phi', 1)
    #----  ----- -----  ------ ----- ----- -----
#=======================================================================
if __name__ == "__main__":
    if TowerMode=='sc':
        Layers=['sc']
    EXT='.coe' # 24

    ###__Create Readme.txt file in savedir________________________________#
    ThisCode=os.path.basename(__file__) # get name of this script when it runs
    print('The running Code was ', ThisCode)
    Reason='To created ultra scale FPGA input data'
    file_name='ReadMe'##+ SaveDirName[-23:]  # 22 last 19 char of SaveDirName[-19:]
    path = os.path.join(SaveDirName, file_name)
    with open(path, 'w') as stream:
        stream.write(('User:'+user+'\r\n'))
        stream.write(('py script start time :'+ str(time_start)+'\r\n'+'\r\n'))
        stream.write(('Data File used :'+ str(datafile)+'\r\n'+'\r\n'))
        stream.write(('The python script ran was :'+ThisCode+'\r\n'))
        stream.write(('The purpose of this run was :'+Reason+'\r\n'))
        stream.write(('save to directory is :'+SaveDirName+'\r\n'))
        stream.write(('TowerMode = :'+TowerMode+'\r\n'))
        stream.write(('LayerType(s) = :'+str(Layers)+'\r\n'))
        # add code start : end Time
    ###__End of Create/write REadMe_data_.txt File =================


#### Fill ea layer types fpga-Input_eta##.coe files........
    for LayerType in Layers:
        print('get ready to loop, for layertype =',LayerType)

        # EtaDataSlicesDict=EtaDataSlicesDictReset # keeps keys sets values back to null string ''

        for event in range(NumOfEvents):
            #if event % 10 == 0:
            #    print('Starting On Event ',event)
            print('Starting On Event ',event)
            datatree.GetEntry(event) # get data for event number
            if TowerMode=='sc':
                if LayerType=='sc':
                    EtT = datatree.scells_Et
                    Et = np.array(EtT,dtype=int)#/1000 ## MeV to GeV, all Et at once
                    binMap=map(modifyEt, Et)
                    Etbin = list(binMap)
                    Towers_In_Event = len(EtT)
                    Eta = datatree.scells_eta
                    Phi = datatree.scells_phi

                    EtaList=[]
                    EtaFile00NameDict={}
                    EtaDataSlicesDict={}
                    EtaDataSlicesDictReset={}
                    EtaFile00NameDictReset={}

                    n=0
                    ### Create fpga_input_eta##.coe FILES.....
                    for eta in Eta:
                        if -EtaSet<=eta<=EtaSet:
                            eta=round(eta,eta_dec)
                            if eta not in EtaList:
                                EtaList.append(eta)
                    #### Create EtaSlice file numbers in dict:
                                EtaFile00NameDict[str(eta)]="{:0>3}".format(n) # generate eta##.coe number name for slcie files
                                EtaDataSlicesDict[str(eta)]=""
                                n=n+1

                    etaLen = n

                    EtaDataSlicesDictReset=EtaDataSlicesDict

                    for LayerType in Layers:
                        for EtaValue in EtaList:
                            with open(SaveDirNameEtaValues+LayerType+'_input_data_eta%s'% EtaValue+EXT, 'a') as f:
                                try:
                                    f.readlines()
                                    print('good')
                                    continue
                                except:
                                    f.write('memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =\r\n') # Old Eg below
                        #--------------------------------------
                            with open(SaveDirNameEtaSlices+LayerType+'_input_data_eta%s'% EtaFile00NameDict[str(EtaValue)]+EXT, 'a') as f: #
                                # test line when output files wrong# f.write('line 241'+'\r\n'+'memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =')#+'\r\n') # Old Eg below
                                f.write('memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =\r\n') # Old Eg below
                        #--------------------------------------
                            with open(SaveDirNameEtaSlices+LayerType+'Sorted_input_data_eta%s'% EtaFile00NameDict[str(EtaValue)]+EXT, 'a') as f: #
                                # test line when output files wrong# f.write('line 241'+'\r\n'+'memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =')#+'\r\n') # Old Eg below
                                f.write('memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =\r\n') # Old Eg below


            EtaDataSlicesDict={}
            EtaDataSlicesDict=EtaDataSlicesDictReset
            triplet=[]

            for tower in range(int(Towers_In_Event)):
                try:
                    EtaValue=round(Eta[tower],eta_dec)
                except:
                    print(Towers_In_Event, tower)
                    quit()
### Build triplet for ea. event ###

                if EtaValue in EtaList:
                    et=Etbin[tower]
                    EtaDataSlicesDict[str(EtaValue)]=EtaDataSlicesDict[str(EtaValue)]+et
                    triplet.append((EtaValue,round(Phi[tower],2),et))

                EtaTripletsDictionary={}
                fpgaEtLine=''
                sorted_by_y = sorted(triplet,key=itemgetter(1))
                sorted_by_y_then_x = sorted(sorted_by_y,key=itemgetter(0))

            for EtaValue in EtaList:
                for i in range(etaLen):
                    if sorted_by_y_then_x[i][0]==EtaValue:
                        fpgaEtLine=fpgaEtLine+sorted_by_y_then_x[i][2]



            if TestPrint=='y':
                print('Line no.',lineno,'TestPrint ON')
                if EtaValue in EtaList:
                    print('EtaDataSlicesDict ',EtaDataSlicesDict[str(EtaValue)])
                else:
                    print('EtaDataSlicesDict ',EtaDataSlicesDict[EtaDataSlicesDict.keys()[0]])

            #### Write the Eta Dictionary Key's Values to fpga_input_eta##.coe files

            for EtaValue in EtaList:
                with open(SaveDirNameEtaValues+LayerType+'_input_data_eta%s'% EtaValue+EXT, 'a') as f: #
            # test line when output files wrong# f.write('line 241'+'\r\n'+'memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =')#+'\r\n') # Old Eg below
                    f.write(EtaDataSlicesDict[str(EtaValue)]+'\r\n') # Old Eg below
        #--------------------------------------
                with open(SaveDirNameEtaSlices+LayerType+'_input_data_eta%s'% EtaFile00NameDict[str(EtaValue)]+EXT, 'a') as f: #
            ## test line when output files wrong# f.write('line 241'+'\r\n'+'memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =')#+'\r\n') # Old Eg below
                    f.write(EtaDataSlicesDict[str(EtaValue)]+'\r\n') # Old Eg below
                EtaDataSlicesDict[str(EtaValue)]=''

                with open(SaveDirNameEtaSlices+LayerType+'Sorted_input_data_eta%s'% EtaFile00NameDict[str(EtaValue)]+EXT, 'a') as f: #
                # test line when output files wrong# f.write('line 241'+'\r\n'+'memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =')#+'\r\n') # Old Eg below
                    f.write(fpgaEtLine+'\r\n') # Old Eg below
            if event % 100 == 0:
                print("Finished Processing Event %s" % event)
                time_point=time_format2 % time.localtime()[0:6]
                with open(path, 'a') as stream:
                    stream.write(('    py script +100 events time :'+ str(time_point)+'\r\n'))
                    print('100 events time : ', time_point)
    print('All layers, loops complete.')
    print('EtaList was = ', EtaList)
    print('Towers_In_Event was : ', Towers_In_Event)
    print(EtaDataSlicesDict)
    #print 'triplet =',triplet,' = triplet'
        #time_format2=str('/%4d_%02d_%02d-%02d:%02d:%02d')
    time_end=time_format2 % time.localtime()[0:6]
    with open(path, 'a') as stream:
        stream.write(('    py script end time :'+ str(time_end)+'\r\n'+'\r\n'))
    print('end time : ', time_end)
