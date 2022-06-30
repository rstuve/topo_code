import numpy as np
import matplotlib.pyplot as plt
import os

folder_name = '2022_06_27-h14-m47-s32_SCntuple;2'
layer_num = folder_name[-1]
path_name = 'root_to_coe/' + folder_name + '/Et_values/'

event = input("Which event?\n> ")


def bin_to_dec(num):
    return int(num,2)

a = []

with open(path_name + '_input_data_et_event' + event + '.coe') as f:
    data = f.readlines()
    for d in data:
        a.append(bin_to_dec(d.strip()))

a = np.asarray(a)
print("Data processed, generating histogram...")
plt.hist(a, bins=100, range=(0,100)) # Range is FILE DEPENDENT
plt.title("scells_Et_Cycle_"+layer_num+"_event_"+event)
plt.xlabel("Tranverse Energy (.01 Gev)")
plt.show()
