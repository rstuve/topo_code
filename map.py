from ROOT import TFile
import matplotlib.pyplot as plt
### END Imports==============================================
layer = 1
filename = '../data/from_jochen/CaloCellsMap.root'
cycle = "caloCellsMap;1"
newFile = '../data/idMap.coe'
#filename = '../data/from_jochen/myfile_tree.root'
#cycle = "ntuple;1"

## 2c) SET DATA FILE/DIR ____________________________
file = TFile(filename)
tree = file.Get(cycle)
tree.GetEntry(0) # reduces tree to single event

samples = tree.cells_sampling
etas = tree.cells_eta
ids = tree.cells_ID

etaGran = 0.0031250000465661287
phiGran = 0.09817477315664291
l = [tuple[1:] for tuple in zip(samples,ids,etas) if tuple[0] == layer and -1.4 <= tuple[2] and tuple[1] <= 765722238]
l.sort()
ids, etas = zip(*l)

lead_etas = []
groups = []
for i in range(len(ids)):
    if (ids[i] - 757072384) % 512 == 0:
        groups.append([])
        lead_etas.append(etas[i])
    groups[-1].append(ids[i])

z = list(zip(lead_etas,groups))
z.sort()

with open(newFile, 'w') as f:
    f.write(f'Layer 1 cell IDs by eta (-1.4 to 1.4) and phi, etaGran = {etaGran}, phiGran = {phiGran} \n')
    for group in z:
        for id in group[1]:
            f.write(f'{id} ')
        f.write('\n')
