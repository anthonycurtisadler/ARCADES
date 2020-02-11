from globalconstants import DASH, PLUS, STAR, EMPTYCHAR, POUND
from indexclass import Index
import datetime


### UTILITIES


def is_date(entry,returndate=False):

    """Utility to test if a string constitutes a date, returning either
    a boolean value or a converted date """

    date_constraints = {0:(-800000000000,+80000000000),
                        1:(1,12),
                        2:(1,31),
                        3:(0,23),
                        4:(0,59),
                        5:(0,59)}
    if isinstance(entry,str) and not entry.replace(DASH,EMPTYCHAR).isnumeric():
        return False
    if isinstance(entry,float):
        return False
    if not isinstance(entry,(tuple,list)):

        if entry and entry[0] == DASH:
            entry = entry[0].replace(DASH,PLUS)+entry[1:]
        entry = entry.split(DASH)

        for x_temp in entry:
            if not x_temp.isnumeric():
                False
        entry = [int(x_temp.replace(PLUS,DASH)) for x_temp in entry]
    

    for counter,x_temp in enumerate(entry):
        if not isinstance(x_temp,int):
            return False
        if not (date_constraints[counter][0]<=x_temp<=date_constraints[counter][1]):
            return False
    if returndate:

        if len(entry) <=3:
            entry += [1,1]
            return datetime.date(entry[0],entry[1],entry[2])
        elif len(entry) <=5:
            entry += [1,1]
            return datetime.datetime(entry[0],entry[1],entry[2],entry[3],entry[4])
    
    return True 

def isindex(entry):

    if not entry:
        return False

    if isinstance(entry,int):
        return True

    if isinstance(entry,str):
        if '..' not in entry and \
           entry[0] != '.' and \
           entry[-1] != '.' and \
           entry.replace('.',EMPTYCHAR).isnumeric():
            return True

    return False

def isfloat(x):
	if x.startswith('-'):
		x=x[1:]
	if x.isnumeric():
		return True
	if x.count('.') == 1:
		if x.replace('.','').isnumeric() and x[-1]!='.':
			return True
	return False


def all_indexes(entrylist):

    for x in entrylist:
        if not isindex(x):
            return False
    return True

def get_type(entrylist):


    type_set = {type(x) for x in entrylist}
    if len(type_set) == 1:
        return list(type_set)[0]
    elif len(type_set) == 0:
        return None
    else:
        if len(type_set) == 2:
            if float in type_set and int in type_set:
                return float      
        return 'INCONSISTENT'

def convert_to_type(item,is_type):
    return_item = None
    if type(item) == is_type:
        return_item = item
    elif is_type == str:
        return_item = str(item)
    elif is_type == type(datetime.date(1972,3,13)) and isinstance(item,str):
        return_item =is_date(item,returndate=True)
    elif is_type == float and isinstance(item,str) and isfloat(item):
        return_item = float(item)
    elif is_type == int and isinstance(item,str) and item.isnumeric():
        return_item = int(item)
    elif is_type == type(Index(0)) and isinstance(item,str) and isindex(item):
        return_item = Index(item)
    elif is_type == float and isinstance(item,int):
        return_item = float(item)
    return return_item

### CLASS DEFINITION


class OrderedList:

    def __init__(self,entrylist=None,indexstrings=False):

        if entrylist and indexstrings:

            self.indexstrings = True 
            self.list = sorted([str(x_temp) for x_temp in entrylist],
                               key=lambda x_temp: Index(str(x_temp)))
            
        elif entrylist and not indexstrings:
            try:
                self.list = sorted(set(entrylist))
            except:
                self.list = entrylist
            self.indexstrings = False
        else:
            self.list = []
            self.indexstrings = indexstrings
        self.sequence_type = None

    def __str__(self):
        if len(self.list)>0:
            if isinstance(self.list[-1], str):
                return ', '.join(["'"+str(x_temp)+"'" for x_temp in self.list])
            elif type(self.list[-1]) == type(Index(0)):
                return ', '.join(["Index('"+str(x_temp)+"')" for x_temp in self.list])
            else:
                return ', '.join([str(x_temp) for x_temp in self.list])
        return ''

    def __len__(self):
        return len(self.list)

    def convert_to_dates(self):

        return_text = EMPTYCHAR 

        def all_dates():
            for x_temp in self.list:
                if type(x_temp) != type(datetime.date(1970,1,7)):
                    return False
            return True

        def all_date_strings():
            for x_temp in self.list:
                if isinstance(x_temp,(float,int)) \
                   or type(x_temp)==type(datetime.date(1970,1,7)) \
                   or type(x_temp)==type(Index(0)):
                    return False
                if isinstance(x_temp,str) and not is_date(x_temp) \
                   and not is_date((x_temp+'-01')) \
                   and not is_date((x_temp+'-01-01')):
                    return False
            return True

        return STAR*all_dates() + POUND*all_date_strings()


    def find(self,item):


        try:
            if self.indexstrings:

                
                if not isinstance(item,str):
                    item = str(item)

                if not self.list: # if the list is empty
                    return False,-1

                if len(self.list) == 1: #if only one value in list which is equal to item
                    if Index(self.list[0]) == Index(item):
                        return True, 0
                    else:
                        if Index(item) > Index(self.list[0]):

                            return False, -2 # if one value in list, greater than item
                        else:

                            return False, -1 #... less than item 
                elif Index(item) < Index(self.list[0]):

                    return False,-1 # if the item is smaller than the least value of the list
                elif Index(item) > Index(self.list[-1]):

                    return False,-2 # if the item is greater than the least value of the list 
                else: # is the item is within the list 
                    # search algorithm 
                    lowest = 0 
                    highest = len(self.list)

                    middle = int((lowest+highest)/2)
  

                    while True:


                        if Index(self.list[middle]) == Index(item):

                            return True,middle
                        if middle in [lowest,highest]:    
                            break

                        if Index(self.list[middle]) < Index(item):
                            lowest = middle
                        else:
                            highest = middle               
                        middle = int((lowest+highest)/2)
                    
                    return False,middle+1 # if the item is not found 

 

        except: # if the ordered list does not in fact consist in indexstrings 
            self.indexstrings = False

        if not self.list:
            return False,-1 # if the list is entry

        if len(self.list) == 1: # for a list with one item
            if self.list[0] == item:
                return True, 0 
            else: 
                if item > self.list[0]:

                    return False, -2 # if item is greater than
                else:

                    return False, -1 # is less then 
        if item < self.list[0]:

            return False,-1 # it item is less than 
        elif item > self.list[-1]:

            return False,-2 # if great then
        else: # search algorithm

            lowest = 0
            highest = len(self.list)

            middle = int((lowest+highest)/2)


            while True:


                if self.list[middle] == item:

                    return True,middle
                if middle in [lowest,highest]:    
                    break

                if self.list[middle] < item:
                    lowest = middle
                else:
                    highest = middle               
                middle = int((lowest+highest)/2)

            return False,middle+1 # if not found 




    def add(self,item):
        if not self.sequence_type or type(item) != self.sequence_type:
            self.sequence_type = get_type(self.list+[item])
        if self.sequence_type == "INCONSISTENT":
            self.sequence_type = get_type(self.list)
        if self.sequence_type is None:
            self.sequence_type = type(item)


        item = convert_to_type(item,self.sequence_type)
        if item:

            try:
                if self.indexstrings:
                    if not isinstance(item,str):
                        item = str(item)

                    if not self.list:
                        self.list  = [item]
                    
                    elif not self.find(item)[0]:
                        if Index(item) < Index(self.list[0]):
                            self.list = [item]+self.list
                        elif Index(item) > Index(self.list[-1]):
                            self.list = self.list+[item]
                        else:
                            index = self.find(item)[1]
                            self.list = self.list[0:index]+[item]+self.list[index:]
                        
            except:
                self.indexstrings =False

            if not self.indexstrings:

                if not self.list:
                    self.list  = [item]
                
                elif not self.find(item)[0]:
                    if item < self.list[0]:
                        self.list = [item]+self.list
                    elif item > self.list[-1]:
                        self.list = self.list+[item]
                    else:
                        index = self.find(item)[1]
                        self.list = self.list[0:index]+[item]+self.list[index:]

    def delete(self,item):

        try:
            if self.indexstrings:
                if not isinstance(item,str):
                    item = str(item)
        except:
            self.indexstrings = False
        if item in self.list:
            self.list.remove(item)

    def index(self,item):
        try:
            if self.indexstrings:
                if not isinstance(item,str):
                    item = str(item)
        except:
            self.indexstrings = False
                
        if item in self.list:
            return self.find(item)[1]
        return False

    def isin(self,item):

        try:
            
            if self.indexstrings:
                if not isinstance(item,str):
                    item = str(item)
        except:
            self.indexstrings = False
                    
        if item in self.list:
            return True
        return False

    def split(self,item):

        try:

            if self.indexstrings:
                if not isinstance(item,str):
                    item = str(item)
        except:
            self.indexstrings = False


        if item not in self.list:
            return False
        splitpoint = self.find(item)[1]
        return self.list[0:splitpoint],self.list[splitpoint+1:]

    def greater_than_equal(self,item,splitonly=False):

        try:
            if self.indexstrings:
                if not isinstance(item,str):
                    item = str(item)
        except:
            self.indexstrings = False
                

        if item not in self.list:

            if self.list:
                if self.indexstrings:
                    if Index(item) < Item(self.list[0]):
                        #for when the entire list is greater than the item
                        if splitonly:
                            return 0
                        return self.list
                    return [x for x in self.list if Index(x) >= Index(item)]
                
                else:
                    if item < self.list[0]:
                        if splitonly:
                            return 0
                        return self.list
            if splitonly:
                return 0
            return []


        splitpoint = self.find(item)[1]

        
        if not splitonly:
            return  self.list[splitpoint:]
        return splitpoint
        

    def lesser_than_equal(self,item,splitonly=False):

        try:
            if self.indexstrings:
                if not isinstance(item,str):
                    item = str(item)
        except:
            self.indexstrings = False

        
        if item not in self.list:
            
            if self.list:
                
                if self.indexstrings:
                    if Index(item) > Index(self.list[-1]):
                        if splitonly:
                            return 0
                        return self.list
                    return [x for x in self.list if Index(x) <= Index(item)]
                else:
                    if item > self.list[-1]:
                        if splitonly:
                            return 0
                        return self.list
                    return [x for x in self.list if x <= item]
            if splitonly:
                return 0
            return []
        splitpoint = self.find(item)[1]
        if not splitonly:
            return self.list[0:splitpoint+1]

        return splitpoint


    def greater_than(self,item,splitonly=False):

        try:
            if self.indexstrings:
                if not isinstance(item,str):
                    item = str(item)
        except:
            self.indexstrings = False
                
        if item not in self.list:
            if self.list:
                if self.indexstrings:
                    if Index(item) < Index(self.list[0]):
                        if splitonly:
                            return 0
                        return self.list
                    return [x for x in self.list if Index(x) > Index(item)]
                else:
                        if item < self.list[0]:
                            if splitonly:
                                return 0
                            return self.list
                        return [x for x in self.list if x > item]
                            
            if splitonly:
                return 0
            return []
            
        splitpoint = self.find(item)[1]

        if not splitonly:
            return self.list[splitpoint+1:]
        return splitpoint+1
       

    def next(self):
        if isinstance(self.list[-1],(int,float)):
            return self.list[-1]+1


    def lesser_than(self,item,splitonly=False):


        try:
            if self.indexstrings:
                if not isinstance(item,str):
                    item = str(item)
        except:
            self.indexstrings = False

        
        if item not in self.list:
            if self.list:
                if self.indexstrings:
                    if Index(item) > Index(self.list[-1]):
                        if splitonly:
                            return 0
                        return self.list
                    else:
                        return [x for x in self.list if Index(x) < Index(item)]
                    
                else:
                    if item > self.list[-1]:
                        if splitonly:
                            return 0
                        return self.list
                    else:
                        return [x for x in self.list if x < item]
            if splitonly:
                return 0
            return []
        splitpoint = self.find(item)[1]
        if not splitonly:
            return self.list[0:splitpoint]
        return splitpoint
       

    def ends (self):
        return self.list[0],self.list[-1]

    def strings (self):
        return [str(a) for a in self.list]

    def find_within(self,item1,item2,fromequal=False,toequal=False):

        try:

            if self.indexstrings:
                if not isinstance(item1,str):
                    item1 = str(item1)
                if not isinstance(item2,str):
                    item2 = str(item2)
                if Index(item1)>Index(item2):
                    item1,item2 = item2,item1
        except:
            self.indexstrings = False

        if not self.indexstrings:
            
            if item1>item2:
                item1,item2 = item2,item1

       

        fromfound, from_temp = self.find(item1)
        tofound, to_temp = self.find(item2)



        if fromfound and not fromequal :
            from_temp += 1
        if tofound and toequal:
            to_temp += 1
        

        if from_temp == -1:
            from_temp = 0

        if to_temp == -1:
            return []
        

        if to_temp != -2 or to_temp <= len(self.list):

            return self.list[from_temp:to_temp]
        else:

            return self.list[from_temp:]
        

        
    def get(self,func_name=None,item=None,item2=None):

        try:

            if self.indexstrings:
                if not isinstance(item,str):
                    item = str(item)
                if not isinstance(item2,str):
                    item2 = str(item2)
        except:
            pass

        # For a single item

        if func_name == '?': #to return all values 
            return self.list        
        if not func_name or not item:
            return []
        if func_name== '=': #to return one value 
            return [item]

        # With two items
        if item2:
            # to get a range

            item2 = convert_to_type(item2,type(item))

            return [x_temp for x_temp in self.greater_than_equal(item) if x_temp <=item2]
            

        if func_name == '>=':
            if not self.indexstrings:
                return [x for x in self.list if x >= item]
            else:
                return [x for x in self.list if Index(x) >= Index(item)]
        elif func_name == '<=':
            if not self.indexstrings:
                return [x for x in self.list if x <= item]
            else:
                return [x for x in self.list if Index(x) <= Index(item)]
        elif func_name == '>':
            if not self.indexstrings:
                return [x for x in self.list if x > item]
            else:
                return [x for x in self.list if Index(x) > Index(item)]
        elif func_name == '<':
            if not self.indexstrings:
                return [x for x in self.list if x < item]
            else:
                return [x for x in self.list if Index(x) < Index(item)]


                





    

    
##a = OrderedList()
##for x in ['1.1','1.2','1.3','1.6','3','5','6']:
##    a.add(Index(x))
##    
##while True:
##    a.add(Index(input('?')))
##    print(str(a))
##    if input('go?') == ' ':
##        break
##
##    
####
####
######for x in [0,2,3,4,24,4477,1000,5,35,434,23]+[387987,3232,44787878,-100,1,7,6,7,8,9,10,2000,3000]:
######    print(x)
######    print(a.find(x))
######    if not a.find(x)[0] and a.find(x)[1]>0:
######        print(a.list[0:a.find(x)[1]],':',a.list[a.find(x)[1]:])
######
######
######while True:
######    a.add(int(input('ADD?')))
######    print(a.list)
######    a.delete(int(input('DELETE?')))
######    print(a.list)
######    print(a.index(int(input('INDEX?'))))
######    print(a.isin(int(input('IS IS?'))))
####
######while True:
######    print(a.split(int(input('='))))
######    print(a.greater_than_equal(int(input('>='))))
######    print(a.greater_than(int(input('>'))))
######    print(a.lesser_than_equal(int(input('<='))))
######    print(a.lesser_than(int(input('<'))))
##while True:
##    print([str(x) for x in a.get(input('FUNC'),Index(input('?')))])
####
