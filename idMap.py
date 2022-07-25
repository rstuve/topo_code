from ROOT import TFile
### END Imports==============================================
layer = 3
filename = '../data/from_jochen/CaloCellsMap.root'
cycle = "caloCellsMap;1"
newFile = '../data/idMap_layer{}.coe'

## 2c) SET DATA FILE/DIR ____________________________
file = TFile(filename)
tree = file.Get(cycle)
tree.GetEntry(0) # reduces tree to single event

for layer in range(4):
    samples = tree.cells_sampling
    mainEtas = tree.cells_eta
    mainIds = tree.cells_ID

    ids, etas = zip(*[tuple[1:] for tuple in zip(samples,mainIds,mainEtas) if tuple[0] == layer])
    minID = ids[0]


    i = list(mainIds).index(minID)
    phiGran = tree.cells_phiGranularity[i]
    etaGran = tree.cells_etaGranularity[i]
    print(etaGran, phiGran)
quit()
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


with open(newFile.format(layer), 'w') as f:
    f.write(f'Layer {layer} cell IDs by eta (-1.4 to 1.4) and phi, etaGran = {etaGran}, phiGran = {phiGran} \n')
    for group in z:
        for id in group:
            f.write(f'{id} ')
        f.write('\n')
