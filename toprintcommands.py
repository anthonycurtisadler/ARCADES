import commandscript

commandlines = commandscript.COMMANDSCRIPT
simple = set()  
ordinary = set()


for x_temp in commandlines:
    for l_temp in x_temp.split('\n'):

        l_temp = l_temp.split('|')+['']
        if l_temp[1].strip() == '':
            simple.update(l_temp[0].split(','))
        else:
            ordinary.update(l_temp[0].split(','))

print('simple')

simple = ', '.join(sorted([s_temp.strip() for s_temp in simple if ' ' not in s_temp.strip()]))

print(simple)

print()
print()
print('ordinary')


ordinary = ', '.join(sorted([s_temp.strip() for s_temp in ordinary if ' ' not in s_temp.strip()]))
print(ordinary)


        
        
