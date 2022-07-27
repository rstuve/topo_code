from ROOT import TFile
import matplotlib.pyplot as plt
### END Imports==============================================
layer = 4
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
mainEtas = tree.cells_eta
mainIds = tree.cells_ID

layers = [0,1,2,3]

lines = []
artists = []
plt.figure(num=1,figsize=(14,7.5))
for i in layers:
    l=[tuple[1:] for tuple in zip(samples,mainIds,mainEtas) if tuple[0] == i]# and -1.4 <= tuple[2] and tuple[1] <= 765722238]
    ids, etas = zip(*l)
    artists.append(plt.scatter(etas,ids,s=1))
    lines.append(f'layer {i}')
plt.legend(artists,lines)
plt.show()
quit()

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
