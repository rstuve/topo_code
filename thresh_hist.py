import numpy as np
import matplotlib.pyplot as plt

no_thresh = np.load('../data/et_lists/event1000_no_thresh.npz')
thresh = np.load('../data/et_lists/event1000_thresh.npz')

no_thresh_counts = []
thresh_counts = []
diffs = []
percents = []
for i in range(4):
    no_thresh_counts.append(len(no_thresh[f'arr_{i}']))
    thresh_counts.append(len(thresh[f'arr_{i}']))
    diffs.append(no_thresh_counts[i]-thresh_counts[i])
    percents.append(diffs[i]/no_thresh_counts[i]*100)

fig, axs = plt.subplots(2, gridspec_kw={'height_ratios': [4, 1]})
fig.set_size_inches(8, 5)
fig.suptitle('Threshold effects on counts per layer')

axs[0].bar([0,1,2,3],thresh_counts,color='b')
axs[0].bar([0,1,2,3],diffs, bottom = thresh_counts,color='r')
axs[0].set_ylabel('ET counts')
axs[0].set_ylim((0,max(no_thresh_counts)*1.05))
axs[0].legend(['no threshold', 'with threshold'])
axs[0].set_xticks([0,1,2,3],[])

axs[1].set_xlabel('layer')
axs[1].set_xticks([0,1,2,3],[0,1,2,3])
axs[1].bar([0,1,2,3],percents, color='r')
axs[1].set_ylabel('% difference')
plt.show()
