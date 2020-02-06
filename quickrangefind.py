import random


pair_list = []
all_indexes = []
for x in range(1000000):
     if random.choice((True,False)):
          all_indexes.append(x)
          

print('calculated')

all_indexes = sorted(all_indexes)
starting = all_indexes[0]
ending = starting


for ind in all_indexes[1:]:

     if ind == ending + 1:
          ending = ind
     elif ind > ending + 1:
          pair_list.append((starting,ending))
          starting = ind
          ending = ind
     else:
          pass
if pair_list[-1] != (starting,ending):
     pair_list.append((starting,ending))
     
result = ''
for pair in pair_list:
     starting,ending = pair[0],pair[1]
     if ending>starting:
          result+=str(starting)+'-'+str(ending)+','
     else:
          result+=str(starting)+','
     

print(result[0:100])

     

     
          
          

     

     

     
