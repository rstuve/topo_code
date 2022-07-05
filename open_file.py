'''
Author: Ryan Stuve
Modified: 6/30/2022

Basic program to open root file, displays event number and data points
Creates variable 'data' which can be studied in >>> python -i open_file.py
'''
import uproot

file = '../data/user.bochen.25650990.OUTPUT._000001.root'
f = uproot.open(file)
tree = f['SCntuple;2']
data = tree.arrays()
print('var "data" is array of arrays of arrays')
print('data has {} entries'.format(len(data)))
print('the different data points are:')
for dataPoint in tree.keys():
    print(dataPoint)
