#!usr/bin/python
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
CreateDir='y' # makes dir to save output to
time_format2=str('/%4d_%02d_%02d-%02d:%02d:%02d')
time_start=time_format2 % time.localtime()[0:6]
print('start time : ', time_start)

user=os.getenv("HOME") #os.path.expanduser('~') # 'mhd' # move to top # can I read user home dir name to set this value ? do it later
print('user is :', user)

## 2b) SET DATA FILE/DIR ____________________________
if user =='/home/luroot' :# home VBox # user =  luroot,  os.getenv("HOME") needs: import os  #
    print('Running over ZHnnbb125 files:') # ZHnnbb125 mu80 (single file) :
   # datafile=TFile('/home/luroot/ROOT_Data/MC15-Samples-00-00-19/               user.cylin.L1CaloSimu.ZvvHbb125.tag-00-00-19_OUTPUT/user.cylin.9015894.OUTPUT._000001.root')
    datafile=TFile('/media/sf_winVBshare/Data_Root/MC15-Samples-00-00-19/user.cylin.L1CaloSimu.ZvvHbb125.tag-00-00-19_OUTPUT/user.cylin.9015894.OUTPUT._000001.root')
elif user =='/home/mhd' :# office del pc
    #datafile=TFile('/home/mhd/ROOT_Data/MC15-Samples-00-00-19/mu80/user.cylin.L1CaloSimu.ZvvHbb125.tag-00-00-19_OUTPUT/user.cylin.9015894.OUTPUT._000001.root')
    datafile=TFile('/home/mhd/Data_Root/MC15-Samples-00-00-19/mu80/user.cylin.L1CaloSimu.ZvvHbb125.tag-00-00-19_OUTPUT/user.cylin.9015894.OUTPUT._000001.root')
elif user =='/export/home/dudley' :# Tier 3 RootData in Topo headprv/..
    datafile=TFile("/headprv/atlas/local/topo/MC15-Samples-00-00-19/user.cylin.L1CaloSimu.ZvvHbb125.tag-00-00-19_OUTPUT/user.cylin.9015894.OUTPUT._000001.root")
else:
    datafile=TFile("user.bochen.25650990.OUTPUT._000001.root")
datatree = datafile.Get("SCntuple;2")
datatree.AddFriend("maps")
# End Set Data input file =========================================
##_ Create/Set Save Directory Folder__________________
if CreateDir=='y':
    CurrentDir=os.getcwd() # print 'The Current working Directory is ',CurrentDir ## #dirfmt = "/root/%4d-%02d-%02d %02d:%02d:%02d" ## #dirfmt = "/%4d_%02d_%02d %02d-%02d-%02d"
    pyScriptName=__file__
    pyScriptNameBase=pyScriptName[:-3] # Remove last 3 char, '.py'
    dirfmt=str(CurrentDir+'/%4d_%02d_%02d-h%02d-m%02d-s%02d'+pyScriptNameBase) #dirfmt=str(CurrentDir+'/%4d_%02d_%02d-%02d-%02d-%02d')
    SaveDirName = dirfmt % time.localtime()[0:6]
    SaveDirName=SaveDirName+'/' #SaveDirName = 'Test_Dir'
    SaveDirNameEtaValues=SaveDirName+'by_eta_values/'
    SaveDirNameEtaSlices=SaveDirName+'by_eta_Slices/'
    SaveDirNameChkTriplets=SaveDirName+'Usual_Triplets_for_chk/'
    try:
        os.mkdir(SaveDirName)
        os.mkdir(SaveDirNameEtaValues)
        os.mkdir(SaveDirNameEtaSlices)
        os.mkdir(SaveDirNameChkTriplets)
        # print 'save to directory is ',SaveDirName
    except OSError:
        # print 'in except, either Dir already exhist or error'
        pass # already exists
    ###_ END :Create/Set Save Directory Folder=====================

## END User Settings  ==========================================================


## 3) FUNCTIONS defs __________________________
def lineno():
    """Returns the current line number in our program."""
    return inspect.currentframe().f_back.f_lineno

def leadingBitn(my_int):
    """ add a leading bit to value, 1 if negative, 0 if positive"""
    nmax=4096 # 12bit Et max
    if 0 <= my_int < nmax:
        return "{0:013b}".format(my_int) # by 13bit auto shove leading 0 for pos number on 12bit number
    elif my_int >= nmax:
        print('n > nmax of',nmax) #4,000,000'
        return "0111111111111" # again leading 0 indicates positve number
    elif my_int <= -nmax:
        return "1111111111111" # again leading 1 indicates negativeitve number
    elif -nmax < my_int < 0:
        #print 'n < nmin of  -', nmax #4,000,000'
        return '1'+"{0:012b}".format(abs(my_int)) # add leading 1 indicates negativeitve number
##__ End : of Declare functions ================================================

TowerMode='sc'
if TowerMode=='j':
    eta_dec=2 # jTowers only needs two decimal palces for eta
    datatree.SetBranchStatus('*', 0)
    datatree.SetBranchStatus('jTowerN', 1)
    datatree.SetBranchStatus('jTowerEt', 1)
    datatree.SetBranchStatus('jTowerEta', 1)
    datatree.SetBranchStatus('jTowerPhi', 1)
    datatree.SetBranchStatus('jTowerEt_EM', 1)
    datatree.SetBranchStatus('jTowerEt_Had', 1)
    #----  ----- -----  ------ ----- ----- -----
    #event=0
    datatree.GetEntry(0) # get data for event number
    Eta = datatree.jTowerEta
    Phi = datatree.jTowerPhi
    #Et = datatree.jTowerEt
    Towers_In_Event=datatree.jTowerN ; print('jTower: Towers_In_jTowerEvent ',Towers_In_Event) # 4224 # 1184# datatree.gTowerN
#=====================================================================
#============================================

if TowerMode=='sc':
    eta_dec=3 # scells need 3 decimal palces for eta
    datatree.SetBranchStatus('*', 0)
    #datatree.SetBranchStatus('jTowerN', 1)
    datatree.SetBranchStatus('scells_Et', 1)
    datatree.SetBranchStatus('scells_eta', 1)
    datatree.SetBranchStatus('scells_phi', 1)
    #datatree.SetBranchStatus('Et_EM', 1)
    #datatree.SetBranchStatus('Et_Had', 1)
    #----  ----- -----  ------ ----- ----- -----
    #event=0
    datatree.GetEntry(0) # get data for event number
    Eta = datatree.scells_eta
    Phi = datatree.scells_phi
    #Et = datatree.jTowerEt
    Towers_In_Event=34048 #datatree.jTowerN ; print 'jTower: Towers_In_jTowerEvent ',Towers_In_Event # 4224 # 1184# datatree.gTowerN
#========================================================================
#####=================================================================###
#=======================================================================
if __name__ == "__main__":
    TestPrint='n' # n=testprint off, 'y'=testprints on
    usualEvents=[]# 0,60,100,400,700,1000]
    EtaSet=2.4
    if TowerMode=='j':
        Layers=['Ave','EM','Had'] #LayerType='Ave'
    if TowerMode=='sc':
        Layers=['sc']
        etaLen=133 #256 # see line 338 for sorting,
    EXT='.coe'
    NumOfEvents=100 # 24

    ###__Create Readme.txt file in savedir________________________________#
    ThisCode=os.path.basename(__file__) # get name of this script when it runs
    print('The running Code was ', ThisCode)
    Reason='To created ultra scale FPGA input data'
    file_name='ReadMe'##+ SaveDirName[-23:]  # 22 last 19 char of SaveDirName[-19:]
    path = os.path.join(SaveDirName, file_name)
    with open(path, 'wb') as stream:
        #stream.write('foo\r\n')
        stream.write(('User:'+user+'\r\n'))
        #dataname=str(datafile)
        stream.write(('py script start time :'+ str(time_start)+'\r\n'+'\r\n'))
        stream.write(('Data File used :'+ str(datafile)+'\r\n'+'\r\n'))
        stream.write(('The python script ran was :'+ThisCode+'\r\n'))
        stream.write(('The purpose of this run was :'+Reason+'\r\n'))
        stream.write(('save to directory is :'+SaveDirName+'\r\n'))
        stream.write(('TowerMode = :'+TowerMode+'\r\n'))
        stream.write(('LayerType(s) = :'+str(Layers)+'\r\n')) #  LayerType+'\r\n'))
        # add code start : end Time
    ###__End of Create/write REadMe_data_.txt File =================

    EtaList=[]
    EtaFile00NameDict={}
    EtaDataSlicesDict={}
    EtaDataSlicesDictReset={}
    EtaFile00NameDictReset={}
    #EtBinString=''
    n=0
    # print 'n ',type(n)
### Create fpga_input_eta##.coe FILES.....
    for eta in Eta:
        #print 'raw eta ',type(eta)
        if -EtaSet<=eta<=EtaSet:
            eta=round(eta,eta_dec)
        #    print 'rnd(eta) ',type(eta)
            #print round(eta,2)
            if eta not in EtaList:
                EtaList.append(eta)
    #### Create EtaSlice file numbers in dict:
            #print n
                #EtaFile00NameDict[str(eta)]="{:0>2}".format(n) # generate eta##.coe number name for slcie files
                EtaFile00NameDict[str(eta)]="{:0>3}".format(n) # generate eta##.coe number name for slcie files
                EtaDataSlicesDict[str(eta)]=""
                n=n+1
    #print 'The Last n =',n
#    print 'just made : EtaSlice Numbers Dict: >',EtaFile00NameDict
#    print 'and       : Eta SliceS Dict >',EtaDataSlicesDict, lineno()
### Create EtaSlice Files
## write header to files for ea. layer type.........
    EtaDataSlicesDictReset=EtaDataSlicesDict
#    EtaFile00NameDictReset=EtaFile00NameDict
#    #if lpAcnt==0:
#     #   lpAcnt=lpAcnt+1
#    print 'EtaDataSlicesDictReset',EtaDataSlicesDictReset
#    print 'EtaFile00NameDictReset',EtaFile00NameDictReset

    for LayerType in Layers:
        for EtaValue in EtaList:
            with open(SaveDirNameEtaValues+LayerType+'_input_data_eta%s'% EtaValue+EXT, 'a') as f: #
                # test line when output files wrong# f.write('line 241'+'\r\n'+'memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =')#+'\r\n') # Old Eg below
                f.write('memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =\r\n') # Old Eg below
        #--------------------------------------
            with open(SaveDirNameEtaSlices+LayerType+'_input_data_eta%s'% EtaFile00NameDict[str(EtaValue)]+EXT, 'a') as f: #
                # test line when output files wrong# f.write('line 241'+'\r\n'+'memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =')#+'\r\n') # Old Eg below
                f.write('memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =\r\n') # Old Eg below
        #--------------------------------------
            with open(SaveDirNameEtaSlices+LayerType+'Sorted_input_data_eta%s'% EtaFile00NameDict[str(EtaValue)]+EXT, 'a') as f: #
                # test line when output files wrong# f.write('line 241'+'\r\n'+'memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =')#+'\r\n') # Old Eg below
                f.write('memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =\r\n') # Old Eg below

#### Fill ea layer types fpga-Input_eta##.coe files........
    for LayerType in Layers:
        print(LayerType)
        print('get ready to loop, for layertype =',LayerType)

        EtaDataSlicesDict=EtaDataSlicesDictReset # keeps keys sets values back to null string ''
#        print 'Layer',LayerType,'.  EtaDataSlicesDict',EtaDataSlicesDict
        #EtBinString=''
        for event in range(NumOfEvents):
            #time.sleep(5)
            if event % 10 == 0:
                print('Starting On Event ',event)
            datatree.GetEntry(event) # get data for event number
            if TowerMode=='j':
                if LayerType=='Ave':
                    Et = datatree.jTowerEt
                    #print 'ave'
                if LayerType=='EM':
                    Et = datatree.jTowerEt_EM
                   # print 'em'
                if LayerType=='Had':
                    Et = datatree.jTowerEt_Had
                    #print 'had'
            if TowerMode=='sc':
                if LayerType=='sc':
                    EtT = datatree.scells_Et
                    Et = np.array(EtT,dtype=int)/1000 ## MeV to GeV, all Et at once
                    #Etbin=map(dec_to_binary, Et)
                    Etbin=map(leadingBitn, Et)
                    print('Et[tower 1]', EtT[1],'int(Et) ',Et[1], ', Et Bin array [1]' ,Etbin[1])
            #print Etbin, ':::EtBin length =',len(Etbin)
            #print Et[1], ':::Et length =',len(Et), '  Max(Et) = ', max(Et)

#            EtaDataSlicesDict={}
#            EtaDataSlicesDict=EtaDataSlicesDictReset
#            triplet=[]
#            #print 'starting loop, so setting triplet set to empty'
#            for tower in range(int(Towers_In_Event)):#datatree.gTowerN
#                EtaValue=round(Eta[tower],2)
#
#                ###USUAL EVENTS SAVE FOR data CHECK::
#                if TowerMode!='sc': # sc=supercell to many towrs slows code too much
#                    if -EtaSet<=EtaValue<=EtaSet:
#                        if event in usualEvents:
#                            with open(SaveDirNameChkTriplets+LayerType+'_EtaPhiPt-Event-%s.txt'%(event), 'a') as f: #
#                           #    f.write(str(Eta[tower])+ ',' + str(Phi[tower])+ ','  + str(Et[tower])+ '\r\n')
#                                f.write(str(EtaValue)+ ',' + str(round(Phi[tower],2))+ ','  + str(int(Et[tower]))+ '\r\n')
#                                #### USUAL EVENTS SAVED.........
#                            ### Build triplet for ea. event ###
#
#
## Make Triplet to sort:

#                if EtaValue in EtaList:
#                    et=leadingBitn(Et[tower])
#
#                    ## BinStringDic
#                    #if oldeta==EtaValue:
#                        #n=n+1
#                    #oldeta=EtaValue
#                    #dictkey(i)Value=value+new-values
#                 #   add=str(n)+', '
#                    EtaDataSlicesDict[str(EtaValue)]=EtaDataSlicesDict[str(EtaValue)]+et
#                    #print 'lentgh of EtaSliceX = ' ,len( EtaDataSlicesDict[str(EtaValue)])#print EtaDataSlicesDict[str(EtaValue)]
#                    #time.sleep(2)
#                    #print 'fill triplet'
#                    triplet.append((EtaValue,round(Phi[tower],2),et))
#                #print triplet,'= triplet'
#                #print n #'len  EtaDataSlicesDict', len(EtaDataSlicesDict)
#                ### Sort (eta,Phi,Et) triplet ###
#                EtaTripletsDictionary={}
#                fpgaEtLine=''
#                sorted_by_y = sorted(triplet,key=itemgetter(1))
#                sorted_by_y_then_x = sorted(sorted_by_y,key=itemgetter(0))
#                #print 'len(EtaList)',len(EtaList)
#                #print 'triplet 261',triplet,'261 triplet'
#                #print 'sorted_by_y,',len(sorted_by_y)
#                #print 'sorted_by_y_then_x =',sorted_by_y_then_x,'= sorted_by_y_then_x'
#                #print 'len(sorted_by_y_then_x =',len(sorted_by_y_then_x)
#           # print 'len(triplet)',len(triplet), '/50',len(triplet)/50
#            for EtaValue in EtaList:
#                #for i in range(64): # 64= len(triplet)/50 , 50=no. of eta slices :: for jTowers
#                for i in range(etaLen): # 64= len(triplet)/50 , 50=no. of eta slices
#                    #print 'i',i
#                    #print 'len(EtaList)',len(EtaList)
#                    if sorted_by_y_then_x[i][0]==EtaValue:
#                        fpgaEtLine=fpgaEtLine+sorted_by_y_then_x[i][2]
#            #print fpgaEtLine
#
#
#
#            if TestPrint=='y':
#                print 'Line no.',lineno,'TestPrint ON'
#                if EtaValue in EtaList:
#                    print 'EtaDataSlicesDict ',EtaDataSlicesDict[str(EtaValue)]
#                else:
#                    print 'EtaDataSlicesDict ',EtaDataSlicesDict[EtaDataSlicesDict.keys()[0]]
#                        #EtaT=round(Eta[tower],2)
#                    #with open(SaveDirNameEtaValues+LayerType+'_input_data_eta%s'%(EtaT) + EXT, 'a') as f: #
#                        #f.write(et)#f.write(str(et)) # Old Eg below
#                    #with open(SaveDirNameEtaSlices+LayerType+'_input_data_eta%s'% EtaSliceDict[str(EtaT)]+EXT, 'a') as f: #
#                        #f.write(et)
#                    #if n =len(EtaSliceDict)
#                #print EtaList
#                #print 'Towers_In_Event', Towers_In_Event
#
#            # cecking Results of term output for above line,
#            # is correct length and format 64 23bit numbers in line of 1472 bits!for jTowers Et,  mhd Saturday, 2016 11 12  21:!5
#            #>>> b='00000000000001011010111000000000000000100111000000000000000001100010000000000000001100111101000000000000001011100000000000000000000000000000000000000000010010100000000000000000000000001000000000000000001000100000000000000100010110000000000000001011100100000000000000000001111000000000000000011101100000000000000010101001000000000000000010011101000000000000000111000010000000000000000110111000000000000000000000000000000000000000000000000000000000000010110000000000000000000000000000000000000000000001100101000000000000011010101110000000000000000100111000000000000001000000001000000000000010010100000000000000000000110110000000000000001001001000000000000000000010100000000000000000000000000000000000000001110010010000000000000001010111000000000000000001111100100000000000000000000000000000000000000000000000000000000000001000101110000000000000100001111000000000000000001111100000000000000100011001000000000000000000000000000000000000000110111000000000000000001111101000000000000000000010000000000000000000110001000000000000000110001100000000000000010110001011000000000000011011111110000000000000010101111000000000000000000111001000000000000000000000000000000000000010001000000000000000000011010010000000000000000000000000000000000000000000000000000000000000101100100000000000000000101110000000000000000000000000000000000000000010001001000000000000000000000000000000000000010001000100000000000000110010100100000000000000000110110000000000001000010001000000000000001100111101'
#            #>>> len(b)
#            #1472
#            #>>> len(b)/23
#            #64
#
#            #### Write the Eta Dictionary Key's Values to fpga_input_eta##.coe files
#
#            for EtaValue in EtaList:
#                with open(SaveDirNameEtaValues+LayerType+'_input_data_eta%s'% EtaValue+EXT, 'a') as f: #
#            # test line when output files wrong# f.write('line 241'+'\r\n'+'memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =')#+'\r\n') # Old Eg below
#                    f.write(EtaDataSlicesDict[str(EtaValue)]+'\r\n') # Old Eg below
#        #--------------------------------------
#                #print 'line 217'
#                #print 'Line no.',lineno
#                #print 'EtaFile00NameDict',EtaFile00NameDict[str(EtaValue)],'EtaFile00NameDict'
#                with open(SaveDirNameEtaSlices+LayerType+'_input_data_eta%s'% EtaFile00NameDict[str(EtaValue)]+EXT, 'a') as f: #
#            ## test line when output files wrong# f.write('line 241'+'\r\n'+'memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =')#+'\r\n') # Old Eg below
#                    f.write(EtaDataSlicesDict[str(EtaValue)]+'\r\n') # Old Eg below
#                EtaDataSlicesDict[str(EtaValue)]=''
#
#                with open(SaveDirNameEtaSlices+LayerType+'Sorted_input_data_eta%s'% EtaFile00NameDict[str(EtaValue)]+EXT, 'a') as f: #
#                # test line when output files wrong# f.write('line 241'+'\r\n'+'memory_initialization_radix =2;'+'\r\n'+'memory_initialization_vector =')#+'\r\n') # Old Eg below
#                    f.write(fpgaEtLine+'\r\n') # Old Eg below
#        if event % 100 == 0:
#            print "Finished Processing Event %s" %(event)
#            time_point=time_format2 % time.localtime()[0:6]
#            with open(path, 'a') as stream:
#                    stream.write(('    py script +100 events time :'+ str(time_point)+'\r\n'))
#            print '100 events time : ', time_point
#    print 'All layers, loops complete.'
#    print 'EtaList was = ', EtaList
#    print 'Towers_In_Event was : ', Towers_In_Event
#    print EtaDataSlicesDict
#    #print 'triplet =',triplet,' = triplet'
#        #time_format2=str('/%4d_%02d_%02d-%02d:%02d:%02d')
    time_end=time_format2 % time.localtime()[0:6]
#    with open(path, 'a') as stream:
#        stream.write(('    py script end time :'+ str(time_end)+'\r\n'+'\r\n'))
    print('end time : ', time_end)
