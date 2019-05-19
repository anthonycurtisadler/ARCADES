## IMPORTED UTILITIES

from globalconstants import LEFTPAREN, RIGHTPAREN, PERIOD
from indexutilities import index_is_reduced, index_reduce, index_expand
from copy import deepcopy

## CLASS DEFINITION

class TranspositionTable:

    def __init__(self,index_list=None):
        

        self.table = {}
        if isinstance(index_list,dict):
            self.table = deepcopy(index_list)
        elif index_list:
            self.table ={str(x_temp):str(x_temp) for x_temp in index_list}

    def __str__ (self):
        return_list = []
        for x_temp in self.table:
            return_list.append(x_temp+':'+self.table[x_temp])
        return ', '.join(return_list)

    def load(self,index_list=None):

        if index_list:
            self.table ={str(x_temp):str(x_temp) for x_temp in index_list}

    def move(self,ind_from,ind_to):
 
        ind_from = str(ind_from)
        ind_to = str(ind_to)
        
        if ind_from in self.table and ind_to not in self.table.values():
            self.table[ind_from] = ind_to
        if ind_from not in self.table and\
           ind_from in self.table.values() and\
           ind_to not in self.table.values():
            for x_temp in self.table:
                if self.table[x_temp] == ind_from:
                    self.table[x_temp] = ind_to

    def transpose(self,index_list=None):
        return_list = []
        for x_temp in index_list:
            if x_temp in self.table:                
                return_list.append(self.table[x_temp])
        return return_list

    def add(self,new_index):
        new_index = str(new_index)
        if new_index not in self.table and new_index not in self.table.values():
            self.table[new_index]=new_index

    def delete(self,to_delete):
        to_delete = str(to_delete)
        if to_delete in self.table:
            del self.table[to_delete]

    def transform(self,new_index,surround=True):
        new_index = str(new_index)
        if new_index in self.table:
            return '<<'*surround+index_reduce(self.table[new_index])+'>>'*surround
        return new_index
    


##starting_list = index_list=input('?').split(',')
##xtable = TranspositionTable(starting_list)
##print(str(xtable))
##while True:
##    xtable.change(input('?'),input('??'))
##    print(str(xtable))
##    print(', '.join(xtable.transpose(starting_list)))
##    if input('delete?') in ['y']:
##        xtable.delete(input('?'))
##    print(str(xtable))
##    if input('add') in ['y']:
##        xtable.add(input('?'))
        
    
