from ROOT import TFile
### END Imports==============================================


## 2c) SET DATA FILE/DIR ____________________________
def makeMap(layer):
    filename = '../data/from_jochen/CaloCellsMap.root'
    cycle = "caloCellsMap;1"
    file = TFile(filename)
    tree = file.Get(cycle)
    tree.GetEntry(0) # reduces tree to single event

    samples = tree.cells_sampling
    mainEtas = tree.cells_eta
    mainPhis = tree.cells_phi
    mainIds = tree.cells_ID

    ids, etas = zip(*[tuple[1:] for tuple in zip(samples,mainIds,mainEtas) if tuple[0] == layer])
    minID = ids[0]


    i = list(mainIds).index(minID)
    phiGran = tree.cells_phiGranularity[i]
    etaGran = tree.cells_etaGranularity[i]
    lineLength = int(3.14*2/phiGran) + bool((3.14*2/phiGran) % 1)


    z = []
    tempID = minID
    negFlag = True
    while True:
        try:
            i = ids.index(tempID)
            if etas[i] < -1.4:
                tempID = ids[i+lineLength]
                negFlag = False
            elif etas[i] > 1.4:
                break
            else:
                if negFlag:
                    z.insert(0,[tempID+j*2 for j in range(lineLength)])
                else:
                    z.append([tempID+j*2 for j in range(lineLength)])
                tempID += 512

        except:
            if negFlag:
                tempID = ids[i+lineLength]
                negFlag = False
                continue
            break

    return z, list(zip(mainIds,mainEtas, mainPhis))
