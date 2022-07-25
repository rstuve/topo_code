from ROOT import TFile
import matplotlib.pyplot as plt
### END Imports==============================================
layer = 1
allowNegEts = True
bit_size = 10 # max size of .coe file entry
overflow_count = 0
neg_count = 0
mapFilename = '../data/from_jochen/CaloCellsMap.root'
mapCycle = 'caloCellsMap;1'
etFilename = '../data/from_jochen/myfile_tree.root'
etCycle = 'ntuple;1' # cells_et
newFileFormat = '../data/etMap_{}.coe'

etaGran = 0.0031250000465661287
phiGran = 0.09817477315664291

def findMax():
    'returns cutoff value for .coe entries'
    binMax = 10**bit_size
    return int(str(binMax),2)

def modifyEt(Et):
    'Modifies and returns binary representations of decimal ET values'
    global overflow_count
    global neg_count
    maxNum = findMax()
    # Can convert Et from Mev to Gev here: Et /= 1000
    if Et < 0:
        neg_count += 1
        Et = 0 if allowNegEts else None # sets all negative values to 0, not tested
    elif Et >= maxNum:
        Et = maxNum - 1 # changes overflow values to max binary value
        overflow_count += 1

    Et = '{0:0{1}b}'.format(int(Et),bit_size) # convert to binary of specified bit size

    return Et

## 2c) SET DATA FILE/DIR ____________________________
mapFile = TFile(mapFilename)
mapTree = mapFile.Get(mapCycle)
mapTree.GetEntry(0) # reduces tree to single event

samples = mapTree.cells_sampling
mainEtas = list(mapTree.cells_eta)
mainIds = list(mapTree.cells_ID)

etFile = TFile(etFilename)
etTree = etFile.Get(etCycle)
numOfEvents = etTree.GetEntries()

for event in range(1):
    etTree.GetEntry(event)
    totalEts = len(etTree.cells_et)
    ets=list(map(modifyEt, etTree.cells_et))
    print(f'Event {event}: threw out {round(neg_count/totalEts*100, 2)}% neg and {round(overflow_count/totalEts*100, 2)}% overflow')
    neg_count = 0
    overflow_count = 0

    l = [tuple[1:] for tuple in zip(samples,mainIds.copy(),mainEtas.copy(), ets) if
    tuple[0] == layer and -1.4 <= tuple[2] and tuple[1] <= 765722238]
    l.sort()
    ids, etas, ets = zip(*l)

    lead_etas = []
    groups = []
    for i in range(len(ids)):
        if (ids[i] - 757072384) % 512 == 0:
            groups.append([])
            lead_etas.append(etas[i])
        groups[-1].append(ets[i])

    z = list(zip(lead_etas,groups))
    z.sort()

    with open(newFileFormat.format(event), 'w') as f:
        f.write(f';Layer 1 event {event} cell ETs by eta (-1.4 to 1.4) and phi, etaGran = {etaGran}, phiGran = {phiGran} \n')
        f.write('memory_initialization_radix =2;\n')
        f.write('memory_initialization_vector =\n')
        for group in z:
            for et in group[1]:
                f.write(et)
            f.write('\n')
