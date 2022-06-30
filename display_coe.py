script = input('script name:\n> ')
folder = input('datetime folder name:\n> ')
file = '_input_data_event'+input('Which event?\n> ')
with open(script+'/'+folder+'/by_event/'+file+'.coe') as f:
    lines = f.readlines()

start = input("From which line?\n> ")
if start == 'all':
    for line in lines:
        print(line, end = '')
else:
    fin = int(input("To which line?\n> "))
    start = int(start)
    for line in lines[start:fin]:
        print(line, end = '')
